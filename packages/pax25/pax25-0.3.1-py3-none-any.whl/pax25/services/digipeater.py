"""
Digipeater system. Will determine whether a digipeating frame is one we need to relay,
and if so, will queue up the digipeated frame with the correct flags marked.
"""

from typing import TYPE_CHECKING

from pax25.ax25.address import Address
from pax25.ax25.frame import Frame
from pax25.ax25.matchers import MatchCall, needs_repeat_from
from pax25.ax25.utils import repeated_for
from pax25.interfaces import Interface

if TYPE_CHECKING:  # pragma: no cover
    from pax25.station import Station


class Digipeater:
    """
    Digipeater class. Manages digipeating functions. Only ever digipeats on the
    interface it hears from.

    This may need to be expanded later to allow for multiple digipeater conditions,
    but for now we assume a single digipeater per station, which responds on the main
    station name with SSID 0.
    """

    def __init__(self, station: "Station", auto_register: bool = True) -> None:
        """Initializes the digipeater."""
        self.station = station
        if auto_register:
            self.register()

    @property
    def address(self) -> Address:
        """
        Gets the repeater address of the station.
        """
        return Address(name=self.station.name, ssid=0)

    def register(self) -> None:
        """
        Registers the digipeater into the Frame Router's matchers.
        """
        matcher = needs_repeat_from(self.address)
        self.station.frame_router.register_matcher(
            "digipeater", MatchCall(matcher=matcher, notify=self.repeat)
        )

    def repeat(self, frame: Frame, interface: Interface) -> None:
        """
        Performs digipeating for a matched frame.
        """
        self.station.frame_router.send_frame(
            interface, repeated_for(self.address, frame)
        )

    def unregister(self) -> None:
        """
        Remove the digipeater from the matchers, effectively disabling it.
        """
        self.station.frame_router.remove_matcher("digipeater")
