"""
Serial KISS reader.
"""

import asyncio
import logging
import os
from asyncio import Queue, Task
from typing import TYPE_CHECKING

from serial import Serial

from pax25.ax25.frame import Frame
from pax25.interfaces.kiss.constants import (
    KISS_CMD_DATA,
    KISS_CMD_FULLDUP,
    KISS_CMD_PERSIST,
    KISS_CMD_SLOTTIME,
    KISS_CMD_TXDELAY,
    KISS_ENDIAN,
)
from pax25.interfaces.kiss.protocol import ax25_frames_from_kiss, kiss_command
from pax25.interfaces.types import (
    Interface,
    SerialSettings,
    TerminalNodeControllerSettings,
)
from pax25.utils import async_wrap, cancel_all

if TYPE_CHECKING:  # pragma: no cover
    from pax25.station import Station


logger = logging.getLogger(__name__)

aprint = async_wrap(print)


def default_tnc_settings() -> TerminalNodeControllerSettings:
    """
    Default settings to send to the TNC.
    """
    return {
        "port": 0,
        "tx_delay": 12,
        "persist": 63,
        "slot_time": 1,
        "full_duplex": 0,
    }


class SerialInterface(Interface[SerialSettings]):
    """
    Interface for KISS serial interaction.
    """

    type = "Serial"

    def __init__(self, name: str, settings: SerialSettings, station: "Station") -> None:
        """
        Initialize a serial interface.
        """
        self.name = name
        self.station = station
        default_path = "COM1" if os.name == "nt" else "/dev/ttyUSB0"
        self.path = settings.get("path", default_path)
        self.baud_rate = settings.get("baud_rate", 9600)
        self.timeout = settings.get("timeout", 1)
        self.write_timeout = settings.get("write_timeout", 2)
        self.rtscts = settings.get("rtscts", False)
        self.dsrdtr = settings.get("dsrdtr", False)
        self.xonxoff = settings.get("xonxoff", False)
        self.exit_kiss = settings.get("exit_kiss", False)
        self.gateway = settings.get("gateway", True)
        self.send_queue: Queue[Frame] = Queue()
        tnc_settings = settings.get("tnc_settings", {})
        tnc_settings.update(default_tnc_settings())
        self.tx_delay = tnc_settings["tx_delay"].to_bytes(1, KISS_ENDIAN)
        self.persist = tnc_settings["persist"].to_bytes(1, KISS_ENDIAN)
        self.slot_time = tnc_settings["slot_time"].to_bytes(1, KISS_ENDIAN)
        self.full_duplex = tnc_settings["full_duplex"].to_bytes(1, KISS_ENDIAN)
        self.port = tnc_settings["port"]
        self.serial: Serial = Serial(
            self.path,
            baudrate=self.baud_rate,
            bytesize=8,
            parity="N",
            stopbits=1,
            rtscts=self.rtscts,
            dsrdtr=self.dsrdtr,
            xonxoff=self.xonxoff,
        )
        self._read_loop: Task[None] | None = None
        self._write_loop: Task[None] | None = None

    @property
    def listening(self) -> bool:
        """
        Returns a bool indicating whether the interface is listening.
        """
        if not self._read_loop:
            return False
        return not self._read_loop.done()

    def start(self) -> None:
        """
        Starts the serial read loop.
        """
        if self.exit_kiss:
            self.exit_kiss_mode()
            return
        self._read_loop = asyncio.ensure_future(self.read_loop())
        self._write_loop = asyncio.ensure_future(self.write_loop())

    def send_settings(self) -> None:
        """
        Send the bytes down serial to configure the TNC.
        """
        # Need to write out the bytes to set up the TNC.
        self.serial.write(
            kiss_command(KISS_CMD_TXDELAY, self.port, self.tx_delay)
            + kiss_command(KISS_CMD_PERSIST, self.port, self.persist)
            + kiss_command(KISS_CMD_SLOTTIME, self.port, self.slot_time)
            + kiss_command(KISS_CMD_FULLDUP, self.port, self.full_duplex)
        )

    def exit_kiss_mode(self) -> None:
        """
        Can be used if we need to exit KISS mode. Note: This might
        differ for different implementations, but works for Kantronics systems.
        """
        self.serial.write(b"\xc0\xff\xc0")

    async def read_loop(self) -> None:
        """
        Connect to the given serial object and then start reading frames.
        """
        self.send_settings()
        async for frame in ax25_frames_from_kiss(
            lambda: async_wrap(self.serial.read)(1)
        ):
            self.station.frame_router.process_frame(self, frame)

    async def write_loop(self) -> None:
        """
        Write loop for serial interface.
        """
        while frame := await self.send_queue.get():
            self.serial.write(kiss_command(KISS_CMD_DATA, self.port, frame.assemble()))

    def send_frame(self, frame: Frame) -> None:
        """
        Send frames out on KISS to the serial device.
        """
        self.send_queue.put_nowait(frame)

    async def shutdown(self) -> None:
        """
        Close the serial connection and stop listening.
        """
        self._read_loop, self._write_loop = await cancel_all(
            [self._read_loop, self._write_loop]
        )
        if self.serial.is_open:
            self.serial.flush()
            self.serial.close()
