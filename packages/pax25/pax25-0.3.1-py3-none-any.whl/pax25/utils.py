"""
Utility functions/coroutines for the pax25 project.
"""

import asyncio
import os
from asyncio import CancelledError, Task
from collections.abc import Callable, Coroutine, Generator, Iterable
from contextlib import suppress
from dataclasses import dataclass
from functools import partial, singledispatch
from typing import (
    TYPE_CHECKING,
    Any,
    ParamSpec,
    TypeVar,
)

if TYPE_CHECKING:  # pragma: no cover
    from pax25.interfaces.types import Interface
    from pax25.station import Station
    from pax25.types import ParameterSettings

P = ParamSpec("P")
R = TypeVar("R")


def async_wrap(func: Callable[P, R]) -> Callable[P, Coroutine[None, None, R]]:
    """
    Wraps a function that requires syncronous operation so it can be awaited instead
    of blocking the thread.

    Shamelessly stolen and modified from:
    https://dev.to/0xbf/turn-sync-function-to-async-python-tips-58nn
    """

    async def run(*args: P.args, **kwargs: P.kwargs) -> R:
        loop = asyncio.get_event_loop()
        part = partial(func, *args, **kwargs)
        return await loop.run_in_executor(None, part)

    return run


class EnumReprMixin:
    """
    Mixin for enums that allows their export to remain copy-pastable for instantiation.
    """

    def __repr__(self) -> str:
        """
        Repr for an Enum that allows for copy-pastable instantiation.
        """
        return f"{self.__class__.__name__}.{self._name_}"  # type: ignore [attr-defined]


def default_parameters() -> "ParameterSettings":
    """
    Default parameters for parameter settings.
    """
    return {"retries": 10, "retry_interval": 5000}


def digipeater_factor(*, interval: int, hops: int, constant: int = 1000) -> int:
    """
    Returns a modified length of time based on the number of digipeaters used.

    Each digipeater increases the amount of time required between retries.
    """
    # For now, assuming this is a straight multiplication factor, though maybe we should
    # add some additional padding for processing time.
    constant = constant if hops else 0
    return (hops + 1) * interval + constant


async def cancel(task: Task[Any]) -> None:
    """
    Cancels a task, and then waits for it to be cleaned up.
    """
    task.cancel()
    with suppress(CancelledError):
        await task


async def cancel_all(tasks: Iterable[Task[Any] | None]) -> list[None]:
    """
    Cancel a series of tasks. Returns a None for each task as they are cancelled,
    useful for closing out optionally running tasks.
    """
    results: list[None] = []
    for task in tasks:
        if task is not None:
            await cancel(task)
        results.append(None)
    return results


@singledispatch
def normalize_line_endings(data: bytes) -> bytes:
    """
    Normalize line endings in a bytestring to be sensible on the target sytem.
    """
    return (
        data.replace(b"\r\n", b"\r")
        .replace(b"\n", b"\r")
        .replace(b"\r", os.linesep.encode("utf-8"))
    )


def generate_nones(times: int | None) -> Generator[None]:
    """
    Generator that yields however many Nones as you specify, or an infinite number
    of Nones if times is None.

    This is primarily to normalize loops that could be either a certain amount of
    iterations or forever.
    """
    if times is None:
        while True:
            yield
    else:
        for _ in range(times):
            yield


@dataclass(kw_only=True, frozen=True)
class PortSpec:
    """
    Named tuple for Interface identities as enumerated by the gateways_for function.
    """

    number: int
    name: str
    type: str


type GatewayDict = dict["Interface", PortSpec]


def gateways_for(station: "Station") -> GatewayDict:
    """
    Retrieve all gateways from a station in numerical order.
    """
    gateways: dict[Interface, PortSpec] = {}
    number = 0
    for key, value in station.interfaces.items():
        if value.gateway:
            number += 1
            gateways[value] = PortSpec(number=number, name=key, type=value.type)
    return gateways
