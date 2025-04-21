"""
CommandRouter module. We use the command router to route commands for the command line
app. Other apps can use it, too, as it's not strictly bound to the command line app.
"""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from pax25.applications.autocomplete import AutocompleteDict
from pax25.applications.parsers import ParseError, string_parser
from pax25.applications.utils import send_message
from pax25.exceptions import ConfigurationError
from pax25.services.connection.connection import Connection

type CommandFunc[P] = Callable[[Connection, "CommandContext[P]"], None]

type CommandMap = dict[str, CommandFunc[object]]


@dataclass(frozen=True, kw_only=True)
class CommandSpec[P]:
    """
    Used for defining commands that are used by the command line app, or any other app
    that follows its conventions for commands.
    """

    command: str
    aliases: tuple[str, ...] = tuple()
    # A long description of the command and its usage.
    help: str
    # The function for this command, when run.
    function: CommandFunc[P]
    parser: Callable[[str], P]


@dataclass()
class CommandContext[P]:
    """
    Context handed to a command.
    """

    spec: CommandSpec[P]
    # The actual command as entered by the user.
    command: str
    args: P


def default_command_func(connection: Connection, context: CommandContext[str]) -> None:
    """
    Default command used by CommandRouter.
    """
    send_message(connection, f"{repr(context.command)} is not a recognized command.")


default_command = CommandSpec[str](
    command="",
    help="",
    function=default_command_func,
    parser=string_parser,
)


class CommandRouter:
    """
    Router object that allows us to quickly route to command functions based on a
    command string sent by a user.
    """

    def __init__(
        self,
        default: CommandSpec[Any] = default_command,
    ) -> None:
        """
        Creates an autocompleting command map that handles
        """
        self.command_store: AutocompleteDict[CommandSpec[Any]] = AutocompleteDict()
        # Canonical listing of all command names, used for checking conflicts.
        self.command_set: set[str] = set()
        # Canonical listing of all aliases, used for checking conflicts.
        self.alias_set: set[str] = set()
        self.default = default

    @property
    def help_available(self) -> bool:
        """
        Returns a boolean indicating if there's a help command installed.
        """
        try:
            results = self.command_store["HELP"]
            # Help command is ambiguous if there's more than 1.
            # This could still be wrong if there is an entry named something like
            # 'helpmeplz' and it's not a help command. But we're going to discount that
            # possibility here. If it ever becomes a real problem we'll refactor this
            # to something more robust.
            return len(results) == 1
        except KeyError:
            return False

    def add(self, *args: CommandSpec[Any]) -> None:
        """
        Add commands to the command router.
        """
        for arg in args:
            command = arg.command.upper()
            aliases = set(alias.upper() for alias in arg.aliases)
            to_check = (command, *aliases)
            for entry in to_check:
                if entry in self.command_set or entry in self.alias_set:
                    existing_spec = self.command_store[entry]
                    raise ConfigurationError(
                        f"Found preexisting entry with conflicting name or "
                        f"aliases when adding spec {repr(arg)}. Conflicting "
                        f"entry was: {repr(existing_spec)}"
                    )
            for entry in to_check:
                self.command_store[entry] = arg
            self.command_set |= {command}
            self.alias_set |= aliases

    def remove(self, *args: CommandSpec[Any]) -> None:
        """
        Remove commands from the command router.
        """
        for arg in args:
            command = arg.command.upper()
            if command not in self.command_store.store:
                raise KeyError(f"Command does not exist, {repr(arg.command)}")
            if self.command_store.store[command] != arg:
                raise KeyError(
                    f"Command {repr(arg.command)} exists, but is for a different spec!"
                )
            del self.command_store[command]
            self.command_set -= {command}
            for alias in arg.aliases:
                del self.command_store[alias.upper()]
                self.alias_set -= {alias.upper()}

    def route(self, connection: Connection, command: str) -> None:
        """
        Routes a user to a command function based on their selection, or gives them
        a hint otherwise.
        """
        segments = command.split(maxsplit=1)
        raw_command = segments[0]
        command = raw_command.upper()
        args = ""
        if len(segments) == 2:
            args = segments[1]
        try:
            candidates = self.command_store[command]
        except KeyError:
            context = CommandContext(command=raw_command, args=args, spec=self.default)
            self.default.function(connection, context)
            return
        if len(candidates) > 1:
            possibilities = sorted(entry[1].command for entry in candidates)
            send_message(
                connection,
                "Ambiguous command. "
                f"Did you mean one of these?: {', '.join(possibilities)}",
            )
            return
        [selection] = candidates
        (_key, spec) = selection
        try:
            parsed_args = spec.parser(args)
            context = CommandContext(command=raw_command, args=parsed_args, spec=spec)
        except ParseError as err:
            error_string = str(err)
            if self.help_available:
                error_string += f"\rTry: help {spec.command}"
            send_message(connection, error_string)
            return
        selection[1].function(connection, context)
