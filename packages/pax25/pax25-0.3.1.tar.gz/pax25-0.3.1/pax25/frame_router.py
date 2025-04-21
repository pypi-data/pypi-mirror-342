"""
The Frame Router routes frames to relevant matching functions used to perform any
protocol work.
"""

from logging import getLogger
from typing import TYPE_CHECKING, Any

from pax25.ax25.address import Address
from pax25.ax25.frame import Frame
from pax25.ax25.matchers import MatchCall
from pax25.exceptions import ConfigurationError

if TYPE_CHECKING:  # pragma: no cover
    from pax25.interfaces import Interface
    from pax25.station import Station


log = getLogger(__name__)


class FrameRouter:
    """
    The Frame queue is a sort of router. It takes in frames from the varying interfaces
    and makes sure they go to their proper destination, whether that be an existing
    connection object or re-transcribed and sent out to another interface.
    """

    def __init__(self, *, station: "Station"):
        self.station = station
        # We keep track of the addresses we are internally watching for here, such
        # as contacts to our internally registered applications.
        self.internal_addresses: dict[Address, set[Interface[Any]]] = {}
        self.matchers: dict[str, MatchCall] = {}

    def process_frame(self, interface: "Interface", frame: Frame) -> None:
        """
        Interfaces call this function to put a new frame in the queue, to be interpreted
        as a received frame.

        This function must be resilient to avoid bringing down the station from one bug.
        """
        # Could change while iterating, since we might do something like register a
        # connection.
        matchers = list(self.matchers.items())
        for key, match_call in matchers:
            try:
                if not match_call.matcher(frame, interface):
                    continue
            except Exception:
                log.exception(
                    "Got error for matcher with key %s:",
                    repr(key),
                )
                continue
            try:
                match_call.notify(frame, interface)
            except Exception:
                log.exception(
                    "Got error for notifier with key %s:",
                    repr(key),
                )
                continue

    def send_frame(self, interface: "Interface", frame: Frame) -> None:
        """
        Send a frame out on a specific interface. For now, there's no advantage to
        using this over the interface's send_frame function, but there may later
        be filters which watch for frames that should be removed.
        """
        interface.send_frame(frame)

    def register_matcher(self, key: str, match_call: MatchCall) -> None:
        """
        Registers a matcher.
        """
        if key in self.matchers:
            log.warning(
                "Existing matcher for key %s, %s, was replaced with new matcher %s. "
                "This may be a collision or a sign of a cleanup issue.",
                repr(key),
                self.matchers[key],
                match_call,
            )
        self.matchers[key] = match_call

    def remove_matcher(self, key: str) -> None:
        """
        Removes a matcher based on its key.
        """
        if key not in self.matchers:
            log.warning(
                "Non-existent key removed, %s. This may indicate that the key was "
                "never registered, or cleanup has been called multiple times "
                "unnecessarily.",
                repr(key),
            )
            return
        del self.matchers[key]

    def next_ssid(
        self,
        *,
        name: str,
        interface: "Interface[Any]",
        ssid: int | None = None,
    ) -> int:
        """
        Given a station name and an interface, produces the next SSID.

        You can give an ssid you would prefer by specifying the ssid argument. If the
        ssid already exists or is invalid, throws an exception. This function is
        used primarily by the station in order to assign SSIDs to applications.
        """
        name = name.upper()
        ssids: set[int] = set()
        for address, interfaces in self.internal_addresses.items():
            if address.name != name:
                continue
            if interface in interfaces:
                ssids |= {address.ssid}
        if ssid is None:
            for candidate in range(16):
                if candidate not in ssids:
                    ssid = candidate
                    break
            else:
                raise ConfigurationError(
                    f"All valid SSIDs on {name}, interface {interface} are taken! "
                    "You may have at most 16 SSIDs, numbered 0-15."
                )
        if not 0 <= ssid <= 15:
            raise ConfigurationError("SSID must be between 0 and 15.")
        if ssid in ssids:
            raise ConfigurationError(
                f"SSID {repr(ssid)} already registered on {interface}!"
            )
        return ssid

    def register_station(
        self, *, interface: "Interface[Any]", address: Address
    ) -> None:
        """
        Registers an address as existing on a particular interface. It can then be
        looked up later for making connections.
        """
        self.internal_addresses[address] = self.internal_addresses.get(
            address, set()
        ) | {interface}
