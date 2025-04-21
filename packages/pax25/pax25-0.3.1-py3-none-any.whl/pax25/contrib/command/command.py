"""
Command line interface for controlling Pax25.
"""

import itertools
from collections.abc import Callable
from dataclasses import dataclass

from pax25 import Application, Station
from pax25 import __version__ as pax25_version
from pax25.applications.help import Help
from pax25.applications.parsers import ParseError, no_arguments, pull_segment
from pax25.applications.router import CommandContext, CommandRouter, CommandSpec
from pax25.applications.utils import build_columns, send_message
from pax25.ax25.address import Address
from pax25.ax25.constants import AX25_REPEATER_MAX
from pax25.ax25.frame import Frame
from pax25.ax25.utils import roll_back_ssid
from pax25.contrib.command.shim import ShimApplication
from pax25.contrib.command.types import CommandLineState, CommandSettings, ShimSettings
from pax25.interfaces import FileInterface, Interface
from pax25.services.connection.connection import Connection, connection_key
from pax25.utils import gateways_for


def default_command_line_settings() -> CommandSettings:
    """
    Generate default settings for the command line application.
    """
    return {"auto_quit": False}


def digipeaters_from_string(string: str) -> tuple[Address, ...]:
    """
    Given a string like 'via SOME-1,THING-2,WAT-3', determine digipeaters.
    """
    string = string.strip()
    if not string:
        return tuple()
    try:
        via, *args = string.split(maxsplit=1)
        if not via.lower() == "via" or not args:
            raise ValueError
    except ValueError as err:
        raise ValueError(
            "Digipeater list broken. Try something like 'via NAME-1,NAME-2'."
        ) from err
    string = args[0]
    addresses = tuple(
        Address.from_string(raw_address.strip()) for raw_address in string.split(",")
    )
    if len(addresses) > AX25_REPEATER_MAX:
        raise ValueError(f"Too many digipeaters. Max is {AX25_REPEATER_MAX}.")
    return addresses


def get_indexed_gateway(station: Station, index: int) -> Interface:
    """
    Wrapper for get_nth_gateway that re-raises an IndexError as a parsing error.
    """
    try:
        return station.get_nth_gateway(index)
    except IndexError as err:
        raise ParseError(str(err)) from err


@dataclass(kw_only=True, frozen=True)
class MakeConnectionSpec:
    """
    Used by the connection parser to pass around distilled arguments.
    """

    destination: Address
    digipeaters: tuple[Address, ...]
    interface: Interface


def create_connection_parser(station: Station) -> Callable[[str], MakeConnectionSpec]:
    """
    Generate a parser for the connection commands. Has to be generated since the
    available interfaces/ports are station-specific.
    """

    def connection_parser(raw_args: str) -> MakeConnectionSpec:
        raw_args = raw_args.strip()
        if not raw_args:
            raise ParseError("Need station address.")

        first_arg, remainder = pull_segment(raw_args)
        # First arg can be either a port number/alias, or the destination station.
        # If no port/alias is specified, then it grabs the default gateway (the first
        # registered interface where gateway is set to True)
        try:
            port_number = int(first_arg)
            interface = get_indexed_gateway(station, port_number)
            raw_destination, remainder = pull_segment(remainder)
        except ValueError:
            if first_arg in station.interfaces:
                interface = station.interfaces[first_arg]
                raw_destination, remainder = pull_segment(remainder)
            else:
                interface = get_indexed_gateway(station, 1)
                raw_destination = first_arg
        try:
            destination = Address.from_string(raw_destination)
        except ValueError as err:
            raise ParseError(str(err)) from err
        if remainder:
            try:
                digipeaters = digipeaters_from_string(remainder)
            except ValueError as err:
                raise ParseError(str(err)) from err
        else:
            digipeaters = tuple()
        return MakeConnectionSpec(
            destination=destination,
            digipeaters=digipeaters,
            interface=interface,
        )

    return connection_parser


class CommandLine(Application[CommandSettings]):
    """
    Command line application. Used to handle things like connecting to other nodes
    or changing settings at runtime.
    """

    connections: dict[Connection, CommandLineState]
    frame_log: list[Frame]
    auto_quit: bool
    router: CommandRouter

    def setup(self) -> None:
        """
        Initial setup.
        """
        self.connections = {}
        settings = default_command_line_settings()
        settings.update(self.settings or {})
        self.settings = settings
        self.auto_quit = settings["auto_quit"]
        # Need to match all frames when monitoring.
        self.station.monitor.register_listener("cmd_monitor", self.frame_listener)
        self.router = CommandRouter()
        self.router.add(Help(self.router).spec)

        self.router.add(
            CommandSpec(
                command="connect",
                help="\r".join(
                    [
                        "Use connect to connect to an outbound station. Examples:",
                        "c FOXBOX            # Connect to a station named FOXBOX, by "
                        "default on SSID 0",
                        "c KW6FOX-3          # Connect to SSID 3 on a station named "
                        "KW6FOX",
                        "c KW6FOX-2 via BOOP # Connect to KW6FOX-2 through an "
                        "intermediary station named BOOP",
                        "c 2 KW6FOX-2 via BOOP # Use port 2 to connect to KW6FOX "
                        "through an intermediary station named BOOP",
                        "",
                        "If no port is specified, uses port 1.See also: PORTS",
                    ]
                ),
                parser=create_connection_parser(self.station),
                function=self.connect,
            ),
            CommandSpec(
                command="ports",
                help="\r".join(
                    [
                        "Usage: PORTS",
                        "",
                        "Lists all available interfaces/ports for connecting to "
                        "outbound stations, including aliases. Aliases are case "
                        "sensative.",
                    ]
                ),
                parser=no_arguments,
                function=self.ports,
            ),
            CommandSpec(
                command="quit",
                help="Closes the session.",
                aliases=("bye",),
                parser=no_arguments,
                function=self.quit,
            ),
            self.station.monitor.command,
        )

    def frame_listener(self, frame: Frame, _interface: Interface) -> bool:
        """
        Frame listener. Subscribes to the monitoring service and consumes frames in
        real time if there's a suitable, connected user.
        """
        for key, value in self.connections.items():
            if key.sudo and isinstance(key.interface, FileInterface):  # noqa: SIM102
                if not (
                    value.connection or self.connection_state_table[key]["command"]
                ):
                    # Send any outstanding.
                    self.dump_logs_to_connection(key)
                    send_message(key, str(frame))
                    return True
        return False

    def dump_logs_to_connection(self, connection: "Connection") -> None:
        """
        Send every log to the connection specified. Used when we disconnect and want
        to see what happened in the interim.
        """
        if not connection.sudo and isinstance(connection.interface, FileInterface):
            return
        logs = self.station.monitor.consume_logs()
        if not logs:
            return
        prefix = len(gateways_for(self.station)) > 1
        for logged_frame in logs:
            frame_string = f"{logged_frame.port.number}:" if prefix else ""
            frame_string += str(logged_frame.frame)
            send_message(connection, frame_string)

    def on_proxy_bytes(self, connection: "Connection", message: bytes) -> None:
        """
        Called by the shim application to indicate that we need to send bytes downstream
        to the connecting station.

        We will eventually need to make this smart enough to stash bytes yet to be sent
        in the case of backgrounding the connection.
        """
        connection.send_bytes(message)

    def ports(self, connection: "Connection", _context: CommandContext[None]) -> None:
        """
        List all ports (interfaces) available for connecting outward.
        """
        headers = ["PORT", "ALIAS", "TYPE"]
        source_gateways = gateways_for(self.station)
        if not source_gateways:
            send_message(
                connection,
                "No gateways configured. You may not connect to outbound stations.",
            )
            return
        gateways = [
            (str(port.number), port.name, port.type)
            for port in source_gateways.values()
        ]
        columns = build_columns(itertools.chain(headers, *gateways), num_columns=3)
        send_message(connection, "\r".join(columns))

    def on_proxy_killed(
        self, connection: "Connection", jump_connection: "Connection"
    ) -> None:
        """
        Called by the shim application to indicate that the connection has been killed.
        """
        self.connections[connection].connection = None
        send_message(
            connection, f"*** Disconnected from {jump_connection.second_party}"
        )
        self.dump_logs_to_connection(connection)
        if self.auto_quit:
            connection.disconnect()

    def set_up_connection(
        self,
        *,
        source_connection: "Connection",
        destination: Address,
        interface: Interface,
        digipeaters: tuple[Address, ...],
    ) -> None:
        """
        Set up an outbound connection to route the user through.
        """
        if source_connection.first_party == source_connection.second_party:
            # Internal connection. No need to cycle the SSID.
            source = source_connection.first_party
        else:
            source = roll_back_ssid(source_connection.first_party)
        key = connection_key(source, destination, interface)
        if key in self.station.connections.table:
            send_message(source_connection, "Route busy. Try again later.")
            return
        send_message(source_connection, f"Connecting to {destination}...")
        connection = self.station.connections.add_connection(
            # We are always the second party, and so we're the ones connecting outbound.
            first_party=source,
            second_party=destination,
            digipeaters=digipeaters,
            interface=interface,
            inbound=False,
            application=ShimApplication(
                name=f"(Shim for {key})",
                station=self.station,
                settings=ShimSettings(
                    proxy_connection=source_connection, upstream_application=self
                ),
            ),
        )
        self.connections[source_connection].connection = connection
        connection.negotiate()

    def connect(
        self,
        connection: "Connection",
        context: CommandContext[MakeConnectionSpec],
    ) -> None:
        """
        Connect to a remote station.
        """
        self.set_up_connection(
            source_connection=connection,
            interface=context.args.interface,
            destination=context.args.destination,
            digipeaters=context.args.digipeaters,
        )

    def quit(self, connection: "Connection", context: CommandContext[None]) -> None:
        """
        Closes the application.
        """
        send_message(connection, "Goodbye!")
        connection.disconnect()

    def run_home_command(self, connection: "Connection", message: str) -> None:
        """
        Match a message for a home command.
        """
        if not message:
            send_message(connection, "cmd:", append_newline=False)
            return
        self.router.route(connection, message)

    def on_startup(self, connection: "Connection") -> None:
        """
        Set up the current connection's state.
        """
        self.connections[connection] = CommandLineState()
        self.dump_logs_to_connection(connection)
        send_message(
            connection,
            f"PAX25 v{'.'.join(pax25_version)} CLI, AGPLv3\rcmd:",
            append_newline=False,
        )

    def on_message(self, connection: "Connection", message: str) -> None:
        """
        Handle command from the user.
        """
        if jump_connection := self.connections[connection].connection:
            jump_connection.send_bytes((message + "\r").encode("utf-8"))
            return
        # Send any outstanding frames that entered while they were typing before
        # giving them a response, so we're not missing any.
        self.dump_logs_to_connection(connection)
        self.run_home_command(connection, message)

    def on_shutdown(self, connection: "Connection") -> None:
        """
        Clean up connection state.
        """
        del self.connections[connection]
