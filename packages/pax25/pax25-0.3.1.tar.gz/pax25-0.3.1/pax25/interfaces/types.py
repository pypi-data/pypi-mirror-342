"""
Defines types used by interfaces.
"""

from dataclasses import dataclass
from typing import (
    IO,
    TYPE_CHECKING,
    Any,
    Generic,
    Literal,
    NotRequired,
    TypedDict,
    TypeVar,
)

from pax25.ax25.frame import Frame
from pax25.types import EmptyDict

if TYPE_CHECKING:  # pragma: no cover
    from pax25.station import Station


S = TypeVar("S", bound=dict[str, Any] | EmptyDict, default=Any)


class Interface(Generic[S]):
    """
    The interface base class, which defines the required functions for an interface.
    All the actual functions must be defined on the subclass-- this base class
    just raises NotImplementedError for all of them.

    Attributes:
        listening: bool flag to indicate whether the interface is up and
            listening for packets.
        name: str name of the interface as instantiated, for internal reference.
        settings: S, a settings dictionary for the interface.
        station: Station the interface is initialized for.
        sudo: Whether this interface can be used for superuser connections.
    """

    name: str
    type: str
    settings: S
    station: "Station"
    # Whether this interface accepts outbound connections that aren't preferred
    # addresses.
    gateway: bool
    sudo: bool = False

    @property
    def listening(self) -> bool:
        """
        Returns a flag indicating that the interface is active and listening.
        """
        raise NotImplementedError  # pragma: no cover

    def __init__(self, name: str, settings: S, station: "Station"):
        """
        Initialize the interface. The interface will be initialized with
        its name, settings, and the station it is being initialized for.

        Under what conditions to set sudo is up to you, but it is set to False by
        default. The sudo flag indicates whether this interface can be used for
        superuser connections.

        It does not automatically mean that connections on this interface will be
        treated as superuser connections, but the base Application class will consider
        a user a superuser if they are connected to an interface while its sudo flag is
        True, and their name matches the station's default name.
        """
        raise NotImplementedError  # pragma: no cover

    def send_frame(self, frame: Frame) -> None:
        """
        Send this frame out on this interface.

        **NOTE**: While this function is a synchronous function, the implementation must
        queue the frame for processing asynchronously. The reason is that if the frame
        is processed synchronously, it will be tied in with the same codepath that sent
        the frame. This can result in unpredictable behavior such as a connection
        sending out another frame before it has a chance to increase its frame counter.
        """
        raise NotImplementedError  # pragma: no cover

    def start(self) -> None:
        """
        Interfaces should implement a 'start' function. This function should create
        the read-loop in a non-blocking manner-- specifically, it should create an async
        loop. See example implementations for how this is done.
        """
        raise NotImplementedError  # pragma: no cover

    async def shutdown(self) -> None:
        """
        This handles any cleanup needed to bring this interface offline, closing
        whatever read loops are in effect.
        """
        raise NotImplementedError  # pragma: no cover


class FileSettings(TypedDict, total=False):
    """
    Settings for the file input.
    """

    input: str | IO[bytes]
    output: str | IO[bytes]
    source_name: str
    source_ssid: int
    destination_name: str
    destination_ssid: int
    auto_shutdown: bool
    # If auto_shutdown is True, also closes the event loop after shutdown.
    stop_loop: bool
    sudo: bool


class ConnectionSpec(TypedDict):
    """
    Specification of an IP-connected target.
    """

    host: str
    port: NotRequired[int]


class TerminalNodeControllerSettings(TypedDict, total=False):
    """
    Settings for the TNC, set up when enabling KISS mode. Check the KISS documentation
    to learn about these settings:

    https://www.ax25.net/kiss.aspx
    """

    port: int
    tx_delay: int
    persist: int
    slot_time: int
    full_duplex: int


class SerialSettings(TypedDict, total=False):
    """
    Settings for serial input.
    """

    path: str
    baud_rate: int
    timeout: int
    write_timeout: int
    rtscts: bool
    dsrdtr: bool
    xonxoff: bool
    gateway: bool
    # Set this to make the TNC leave kiss mode and immediately shut down the station.
    # Works for Kantronics.
    exit_kiss: bool
    tnc_settings: TerminalNodeControllerSettings


class TCPSettings(TypedDict, total=False):
    """
    Settings for the TCP interface
    """

    # Inbound settings.
    allow_inbound: bool
    listening_address: str
    listening_port: int

    # Outbound settings.
    call_sign: str
    password: int
    connections: list[ConnectionSpec]

    gateway: bool


class DummySettings(TypedDict, total=False):
    """
    Settings for the dummy system.
    """

    gateway: bool


class FileInterfaceConfig(TypedDict):
    """
    Configuration for file interface.
    """

    type: Literal["file"]
    settings: FileSettings


class DummyInterfaceConfig(TypedDict):
    """
    Configuration for dummy interface.
    """

    type: Literal["dummy"]
    settings: DummySettings


class SerialInterfaceConfig(TypedDict):
    """
    Configuration for the serial interface.
    """

    type: Literal["serial"]
    settings: SerialSettings


class TCPInterfaceConfig(TypedDict):
    """
    Configuration for the TCP Interface.
    """

    type: Literal["tcp"]
    settings: TCPSettings


# Type used for tracking the tty settings we manipulate when we use stdin.
TerminalSettings = list[int | list[bytes | int]]


@dataclass(kw_only=True, frozen=True)
class ResolvedConnectionSpec:
    """
    Variant of ConnectionSpec where we've made sure both host and port are set.
    """

    host: str
    port: int
