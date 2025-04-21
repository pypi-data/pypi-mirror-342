"""
The file interface. This is used mostly for testing-- we can send in predefined
commands and let the system process them this way.

It's also useful for running apps over stdin/stdout, which are the default input/output
files.
"""

import asyncio
import logging
import os
from asyncio import Queue, Task
from contextlib import suppress
from sys import stdin, stdout
from typing import IO, TYPE_CHECKING, Literal, TextIO

from pax25.ax25.address import Address, AddressHeader, Route
from pax25.ax25.constants import AX25_PID_TEXT, SFrameType, UCommand
from pax25.ax25.control import Info, Supervisory, Unnumbered
from pax25.ax25.frame import Frame
from pax25.interfaces.types import FileSettings, Interface
from pax25.services.connection.variables import RolloverCounter
from pax25.utils import async_wrap, cancel_all, normalize_line_endings

if TYPE_CHECKING:  # pragma: no cover
    from pax25.station import Station


logger = logging.getLogger(__name__)


class FileInterface(Interface[FileSettings]):
    """
    A file interface that will read in on a file and send the resulting
    bytes to another file. By default, input is stdin, and output is stdout.

    You may want to set the sudo settings flag to True if this is intended to be the
    administrative connection. Privileges will only be elevated if this flag is true
    AND the 'source ssid' argument matches the station name, which it will by default.
    """

    type = "File"

    def __init__(self, name: str, settings: FileSettings, station: "Station"):
        self.name = name
        self.settings = settings
        self.station = station
        self.input: IO[bytes] | None = None
        self.output: IO[bytes] | None = None
        self.output_tty = False
        self.close_input = False
        self.close_output = False
        self.sudo = settings.get("sudo", False)
        self.gateway = False
        self._read_loop: Task[None] | None = None
        self._write_loop: Task[None] | None = None
        self.vs = RolloverCounter(name="Send State Variable")
        self.vr = RolloverCounter(name="Receive State Variable")
        self.send_queue: Queue[Frame] = Queue()

    @property
    def listening(self) -> bool:
        """
        Returns a bool indicating whether the interface is listening.
        """
        if not self._read_loop:
            return False
        return not self._read_loop.done()

    def handle_for(
        self,
        file_path: str | IO[bytes] | None,
        mode: Literal["r", "w"],
        *,
        default_interface: TextIO,
    ) -> IO[bytes]:
        """
        Gets the file handle for a specified file path, falling back to an interface
        if the path is falsy.
        """
        handle: IO[bytes] = default_interface.buffer
        if file_path:
            if isinstance(file_path, str):
                handle = open(  # noqa: SIM115
                    file_path,
                    f"{mode}b",
                )
            else:
                handle = file_path
        if handle.isatty():  # pragma: no cover
            # We need to massage output if we're displaying to a user's terminal,
            # since pax25's native line endings are JUST carriage returns. This
            # means that on modern systems, be they Windows or *NIX, the line will
            # just keep overwriting itself.
            self.output_tty = True

        return handle

    @property
    def route(
        self,
    ) -> Route:
        """
        Shorthand function for adding the first and second party to the frames we
        construct.
        """
        return Route(
            src=AddressHeader(
                address=Address(
                    name=self.settings.get("source_name", self.station.name),
                    ssid=self.settings.get("source_ssid", 0),
                )
            ),
            dest=AddressHeader(
                address=Address(
                    name=self.settings.get("destination_name", self.station.name),
                    ssid=self.settings.get("destination_ssid", 0),
                )
            ),
        )

    def send_receive_ready(self) -> None:
        """
        Send receive ready. Potentially important if we're not sending but just
        receiving for a while.
        """
        self.station.frame_router.process_frame(
            self,
            Frame(
                route=self.route,
                control=Supervisory(
                    frame_type=SFrameType.RECEIVE_READY,
                    receiving_sequence_number=self.vr.value,
                ),
                pid=None,
            ),
        )

    def send_frame(self, frame: Frame) -> None:
        """
        Add a frame to the queue for processing.
        """
        self.send_queue.put_nowait(frame)

    async def write_loop(self) -> None:
        """
        Handle the frames that have been sent back to us for writing.
        """
        while frame := await self.send_queue.get():
            self.handle_received_frame(frame)

    def handle_received_frame(self, frame: Frame) -> None:
        """
        Handles a frame from the Frame Router. We only care about a handful of frame
        types.
        """
        match frame.control:
            case Info():
                if not self.output:  # pragma: no cover
                    raise RuntimeError(
                        "Received a frame, but we don't have an open output file!",
                    )
                info = frame.info
                if self.output_tty:  # pragma: no cover
                    # Normalize line endings, in the case someone send
                    info = normalize_line_endings(info)
                self.output.write(info)
                self.output.flush()
                self.vr.increment()
                # Always send receive ready since we have zero lag time and may not have
                # another frame available.
                self.send_receive_ready()
            case Unnumbered() as control:
                match control.command:
                    case UCommand.DISCONNECT:
                        self.station.frame_router.process_frame(
                            self,
                            Frame(
                                route=self.route,
                                control=Unnumbered(
                                    command=UCommand.UNNUMBERED_ACKNOWLEDGE
                                ),
                                pid=None,
                            ),
                        )
                        asyncio.ensure_future(self.conditional_shutdown(remote=True))

    async def conditional_shutdown(self, remote: bool = False) -> None:
        """
        If set to shut down the station automatically, go ahead and do so.
        """
        if self.settings.get("auto_shutdown", True) or remote:
            if self.station.closing:
                # Already shutting down.
                return
            await self.station.shutdown(
                stop_loop=self.settings.get("stop_loop", True),
            )

    def start(self) -> None:
        """
        Starts the read loop and schedules it.
        """
        self.input = self.handle_for(
            self.settings.get("input"),
            "r",
            default_interface=stdin,
        )
        self.output = self.handle_for(
            self.settings.get("output"),
            "w",
            default_interface=stdout,
        )
        assert self.input
        assert self.output
        self.close_input = self.input.seekable()
        self.close_output = self.output.seekable()
        # This will create the connection in the connection table.
        self._read_loop = asyncio.ensure_future(self.read_loop())
        self._write_loop = asyncio.ensure_future(self.write_loop())

    async def read_loop(self) -> None:
        """Reads input from the keyboard and sends it for routing."""
        assert self.input
        # If we're reading from stdin, there could be long delays between characters
        # (keystrokes) so we read in 1 byte at a time as a full message frame. The
        # reads block in their own thread to allow other tasks to run. This prevents
        # the application from freezing while waiting for keyboard input.
        read_amount = 256 if self.close_input else 1
        self.station.frame_router.process_frame(
            self,
            Frame(
                route=self.route,
                control=Unnumbered(command=UCommand.SET_ASYNC_BALANCED_MODE),
                pid=None,
            ),
        )
        while True:
            # Note: When reading from a TTY, we don't get ANY characters until the
            # user presses the return key. We will eventually need to handle cases like
            # pressing ctrl+c to exit connection mode but that hasn't been implemented
            # yet.
            message = await async_wrap(self.input.read)(read_amount)
            if self.input.isatty():  # pragma: no cover
                # If we're reading in from a terminal, we need to normalize input.
                # Need to check how this behaves on Windows.
                if os.name == "nt":
                    message = message.replace(b"\r", b"")
                message = message.replace(b"\n", b"\r")
                if not message:
                    continue
            if not message:
                if self.settings.get("auto_shutdown", True):
                    # The file has ended.
                    self.station.frame_router.process_frame(
                        self,
                        Frame(
                            route=self.route,
                            control=Unnumbered(command=UCommand.DISCONNECT),
                            pid=None,
                        ),
                    )
                    await self.conditional_shutdown()
                break
            frame = Frame(
                route=self.route,
                control=Info(
                    receiving_sequence_number=self.vr.value,
                    sending_sequence_number=self.vs.value,
                ),
                pid=AX25_PID_TEXT,
                info=message,
            )
            self.station.frame_router.process_frame(
                self,
                frame,
            )
            self.vs.increment()

    async def shutdown(self) -> None:
        """Closes the read loop, closes open file handles."""
        self._read_loop, self._write_loop = await cancel_all(
            [self._read_loop, self._write_loop]
        )
        if self.close_input and self.input:
            self.input.close()
        if self.output and not self.output.closed:
            # Can happen if the file closes between the await and now.
            with suppress(ValueError):
                await async_wrap(self.output.flush)()
            if self.close_output:
                self.output.close()
