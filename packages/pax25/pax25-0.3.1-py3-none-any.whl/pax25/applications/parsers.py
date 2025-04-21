"""
Included generic parser functions which can be used by client developer commands.
"""

from collections.abc import Callable
from typing import TypeVar

from pax25.applications.autocomplete import AutocompleteDict


def string_parser(args: str) -> str:
    """
    Returns the stripped argument string without further modification.
    """
    return args.strip()


def no_arguments(args: str) -> None:
    """
    Use when a command accepts no arguments.
    """
    if args.strip():
        raise ParseError("This command takes no arguments.")
    return None


def pull_segment(args: str) -> tuple[str, str]:
    """
    Splits a string once and returns the first segment as well as the remainder.
    """
    result = args.split(maxsplit=1)
    segment = result.pop(0)
    remainder = result[0] if result else ""
    return segment, remainder


class ParseError(Exception):
    """
    Throw when there is a parsing error.
    """


E = TypeVar("E", bound=str)


def autocompleted_enum(
    options: tuple[E, ...], *, default: E | None = None
) -> Callable[[str], E]:
    """
    A parser which will return a normalized entry.
    """
    lookup: AutocompleteDict[E] = AutocompleteDict()
    for entry in options:
        lookup[entry.lower()] = entry

    def parse_enum(value: str) -> E:
        """
        Return which entry in the options was used, if any.
        """
        value = value.strip().lower()
        if not value:
            if default is not None:
                return default
            raise ParseError(f"Argument must be one of: {options}")
        try:
            results = lookup[value]
            possibilities = list(sorted(result[1] for result in results))
            if len(results) > 1:
                raise ParseError(
                    f"Ambiguous argument. Could be: {', '.join(possibilities)}"
                )
            result = possibilities[0]
            return result
        except KeyError as err:
            raise ParseError(f"Argument must be one of: {', '.join(options)}") from err

    return parse_enum
