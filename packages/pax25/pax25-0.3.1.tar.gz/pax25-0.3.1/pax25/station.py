"""Station class. Defines the station parameters."""

import asyncio
import logging
from asyncio import Future
from collections import defaultdict
from typing import Any, cast

from pax25.applications import BaseApplication
from pax25.applications.types import S
from pax25.ax25.address import Address
from pax25.exceptions import ConfigurationError
from pax25.frame_router import FrameRouter
from pax25.interfaces import INTERFACE_TYPES, Interface
from pax25.services.connection.service import ConnectionService
from pax25.services.digipeater import Digipeater
from pax25.services.monitor import Monitor
from pax25.types import StationConfig
from pax25.utils import default_parameters

logger = logging.getLogger(__name__)


class Station:
    """
    The main station class for Pax25. This class is intended to manage a physical
    station's digital affairs.
    """

    def __init__(self, *, config: StationConfig):
        self.name = config["name"].upper()
        self.interfaces: dict[str, Interface[Any]] = {}
        for key, value in config["interfaces"].items():
            if key.split() != [key]:
                raise ConfigurationError(
                    f"Interface keys may not have spaces. Got: {repr(key)}",
                )
            interface_cls = INTERFACE_TYPES[value["type"]]
            interface_cls = cast(type[Interface[Any]], interface_cls)
            self.interfaces[key] = interface_cls(
                name=key, settings=value["settings"], station=self
            )
        self.frame_router = FrameRouter(station=self)
        self.digipeater = Digipeater(station=self)
        self.connections = ConnectionService(station=self)
        self.monitor = Monitor(station=self, settings=config.get("monitoring"))
        self.application_map: defaultdict[str, dict[Address, BaseApplication[Any]]] = (
            defaultdict(lambda: {})
        )
        self.closing = False
        self.parameters = config.get("parameters", default_parameters())
        # Timers may get cancelled and the station may shut down before they would
        # be cleaned up normally. We track these tasks so if we shut down while any
        # are still active, we can reap them manually.
        self._active_future: Future[None] | None = None

    @property
    def running(self) -> bool:
        """
        Returns if the station is currently running.
        """
        if self._active_future is None:
            return False
        return not self._active_future.done()

    async def finished(self) -> None:
        """
        Await this to wait until the server is closed down programmatically.
        """
        if self._active_future is None:
            raise RuntimeError(
                "Station has not run. We cannot wait for it to finish if "
                "it never began!"
            )
        await self._active_future

    def run(self) -> None:
        """
        Runs the station. Right now this only brings up all interfaces, but it could
        handle other tasks if we need them later.
        """
        self.bring_up_interfaces()
        self._active_future = asyncio.Future()

    def bring_up_interfaces(self) -> None:
        """
        Attempts to bring up all interfaces and queue them into the event loop.
        """
        for interface in self.interfaces.values():
            interface.start()

    def get_nth_gateway(self, index: int) -> "Interface":
        """
        Get the nth gateway or raise an IndexError if not present.
        """
        if index <= 0:
            raise IndexError("Port numbers start at 1.")
        current = 0
        for interface in self.interfaces.values():
            if interface.gateway:
                current += 1
                if current == index:
                    return interface
        if not current:
            raise IndexError("No gateways available.")
        raise IndexError(f"Port {index} not found.")

    def register_app(
        self,
        app: type[BaseApplication[S]],
        *,
        interfaces: list[str],
        application_name: str | None = None,
        station_name: str | None = None,
        ssid: int | None = None,
        settings: S,
    ) -> BaseApplication[S]:
        """
        Registers a new application to the specified interfaces.
        """
        station_name = (station_name if station_name else self.name).upper()
        application_name = (
            application_name if application_name is not None else app.__class__.__name__
        )
        application_instance = app(
            name=application_name,
            settings=settings,
            station=self,
        )
        for interface in interfaces:
            if interface not in self.interfaces:
                raise ConfigurationError(
                    "Attempted to register application to non-existent "
                    f"interface, {repr(interface)}.",
                )
            new_address = Address(
                name=station_name,
                ssid=self.frame_router.next_ssid(
                    interface=self.interfaces[interface], name=station_name, ssid=ssid
                ),
            )
            self.application_map[interface][new_address] = application_instance
            self.frame_router.register_station(
                interface=self.interfaces[interface], address=new_address
            )
        return application_instance

    async def shutdown(self, stop_loop: bool = False) -> None:
        """
        Shut down all interfaces, cutting off the station.
        """
        if not self.running:
            # Already shut down.
            return
        self.closing = True
        await self.connections.shutdown()
        for interface in self.interfaces.values():
            await interface.shutdown()
        if self._active_future:
            self._active_future.set_result(None)
        self.closing = False
        if stop_loop:  # pragma: no cover
            asyncio.get_event_loop().stop()
