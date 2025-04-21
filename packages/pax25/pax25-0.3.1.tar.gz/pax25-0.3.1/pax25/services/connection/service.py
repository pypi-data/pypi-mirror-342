"""
Connection service. Keeps track of the connection table, instantiates connections,
performs other housekeeping around them.
"""

from typing import TYPE_CHECKING, Any

from pax25.applications import BaseApplication
from pax25.ax25.address import Address
from pax25.ax25.constants import UCommand
from pax25.ax25.frame import Frame
from pax25.ax25.matchers import U_FRAME_CHECKS, MatchCall, check_all, repeats_completed
from pax25.interfaces import Interface
from pax25.services.connection.connection import (
    Connection,
    ConnectionKey,
    connection_key,
)

if TYPE_CHECKING:  # pragma: no cover
    from pax25.station import Station


class ConnectionService:
    """
    Connection handling service.
    """

    def __init__(self, station: "Station", auto_register: bool = True) -> None:
        """
        Initialize the connection service.
        """
        self.station = station
        if auto_register:
            self.register()
        self.table: dict[ConnectionKey, Connection] = {}

    def connection_matcher(self, frame: Frame, interface: Interface) -> bool:
        """
        Matches incoming connection frames.
        """
        if not check_all(
            repeats_completed, U_FRAME_CHECKS[UCommand.SET_ASYNC_BALANCED_MODE]
        )(frame, interface):
            return False
        return frame.route.dest.address in set(
            self.station.application_map.get(interface.name, [])
        )

    def register(self) -> None:
        """
        Register the matchers for the connection service.
        """

        self.station.frame_router.register_matcher(
            "connection",
            MatchCall(matcher=self.connection_matcher, notify=self.inbound_connect),
        )

    def inbound_connect(self, frame: Frame, interface: Interface) -> None:
        """
        Add a connection to the connection table based on an incoming frame.
        """
        first_party = frame.route.src.address
        second_party = frame.route.dest.address
        digipeaters = tuple(
            digipeater.address for digipeater in frame.route.digipeaters
        )
        key = connection_key(first_party, second_party, interface)
        if key in self.table:
            # Existing connection will handle this.
            return
        connection = self.add_connection(
            first_party=frame.route.src.address,
            second_party=frame.route.dest.address,
            interface=interface,
            digipeaters=digipeaters,
            inbound=True,
        )
        connection.negotiate()

    def add_connection(
        self,
        *,
        first_party: Address,
        second_party: Address,
        digipeaters: tuple[Address, ...] = tuple(),
        interface: Interface,
        inbound: bool,
        application: BaseApplication[Any] | None = None,
    ) -> Connection:
        """
        Add a connection to the connection table. Returns a connection if one already
        exists. Note that an existing connection may be outbound rather than inbound,
        or vice versa.
        """
        key = connection_key(first_party, second_party, interface)
        if key in self.table:
            raise ConnectionError(f"Connection already exists! {self.table[key]}")
        if not application and inbound:
            application = self.station.application_map[interface.name][second_party]
        connection = Connection(
            first_party=first_party,
            second_party=second_party,
            digipeaters=digipeaters,
            interface=interface,
            application=application,
            station=self.station,
            service=self,
            inbound=inbound,
            sudo=interface.sudo,
        )
        self.table[key] = connection
        return connection

    def remove_connection(self, connection: Connection) -> None:
        """
        Removes a connection from the connection table.
        """
        key = connection_key(
            connection.first_party, connection.second_party, connection.interface
        )
        del self.table[key]

    def unregister(self) -> None:
        """
        Removes the matchers for the connection service, preventing new connections.
        """
        self.station.frame_router.remove_matcher("connection")

    async def shutdown(self) -> None:
        """
        Shutdown the connection service, closing out all connections.
        """
        self.unregister()
        for connection in list(self.table.values()):
            connection.shutdown()
