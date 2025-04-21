"""
Utility functions for working with AX.25 frames.
"""

from collections.abc import Callable
from dataclasses import replace
from typing import TYPE_CHECKING, TypeVar, cast

from pax25.ax25.address import Address, AddressHeader
from pax25.ax25.control import Info, Supervisory, Unnumbered

if TYPE_CHECKING:  # pragma: no cover
    from pax25.ax25.frame import Frame
    from pax25.ax25.protocols import ControlField


def should_repeat_for(address: Address, frame: "Frame") -> bool:
    """
    Checks if a given address is next in the digipeater list and this frame requires
    repeating.
    """
    for header in frame.route.digipeaters:
        if header.command_or_repeated:
            continue
        if header.address == address:
            return True
        # If we're not next in the repeater list, we don't need to repeat.
        break
    return False


def repeated_for(address: Address, frame: "Frame") -> "Frame":
    """
    Returns a revised frame with the repeat flag set for the specific address.
    Raises if this address isn't a repeater for the frame.
    """
    digipeater_list = list(frame.route.digipeaters)
    address_seen = False
    for index, envelope in enumerate(digipeater_list):
        if envelope.address != address:
            continue
        address_seen = True
        if not envelope.command_or_repeated:
            new_envelope = replace(envelope, command_or_repeated=True)
            digipeater_list[index] = new_envelope
            new_route = replace(frame.route, digipeaters=tuple(digipeater_list))
            return replace(frame, route=new_route)
    if address_seen:
        raise ValueError(
            f"{address} is in the digipeater list, "
            f"but all occurrences are marked repeated.",
        )
    raise ValueError(f"{address} is not a digipeater for {frame}.")


def reply_digipeaters(
    digipeaters: tuple[AddressHeader, ...],
) -> tuple[AddressHeader, ...]:
    """
    Returns a revised frame that has the digipeaters in reverse order and the repeated
    flags all set to False.
    """
    revised_digipeaters = [
        replace(envelope, command_or_repeated=False)
        for envelope in reversed(digipeaters)
    ]
    if revised_digipeaters:
        revised_digipeaters[-1] = replace(revised_digipeaters[-1])
    return tuple(revised_digipeaters)


def response_frame(frame: "Frame") -> "Frame":
    """
    Generates the base of a response frame-- source and destination are swapped,
    digipeaters reversed, and contents emptied. The control is unchanged, as context
    for changes to it would be kept elsewhere.

    The command_or_repeated flag is swapped along with the addresses
    (if it is set at all), so bear this in mind.
    """
    route = frame.route
    route = replace(
        route,
        src=route.dest,
        dest=route.src,
        digipeaters=reply_digipeaters(route.digipeaters),
    )
    return replace(frame, route=route, info=b"")


T = TypeVar("T")


def build_receive_modifier(new_number: int) -> Callable[["Frame"], "Frame"]:
    """
    Creates a modifier function that will replace an information or supervisory frame's
    receive control number with the `new_number` specified.
    """

    def update_receive_number(frame: "Frame") -> "Frame":
        match frame.control:
            case Supervisory() | Info():
                return replace(
                    frame,
                    control=replace(
                        frame.control, receiving_sequence_number=new_number
                    ),
                )
            case _:
                # Unnumbered, no need to update.
                return frame

    return update_receive_number


C = TypeVar("C", bound="ControlField")


def flagged_control(control: C) -> C:
    """
    Marks the poll/response bit for this frame, or raises if we're an info frame.
    """
    match control:
        case Supervisory():
            control = cast(C, replace(control, poll_or_final=True))
        case Unnumbered():
            control = cast(C, replace(control, poll_or_final=True))
        case _:
            raise ValueError(
                f"{control.__class__.__name__} control fields cannot be "
                f"marked as command/response."
            )
    return control


def response(frame: "Frame") -> "Frame":
    """
    Mark the frame as a 'Response' frame, replying to a command frame.
    """
    frame = replace(frame, control=flagged_control(frame.control))
    return replace(
        frame,
        route=replace(
            frame.route,
            src=replace(frame.route.src, command_or_repeated=True),
            dest=replace(frame.route.dest, command_or_repeated=False),
        ),
    )


def command(frame: "Frame") -> "Frame":
    """
    Mark the frame as a 'Command' frame, sent from the source to the destination.
    """
    frame = replace(frame, control=flagged_control(frame.control))
    return replace(
        frame,
        route=replace(
            frame.route,
            src=replace(frame.route.src, command_or_repeated=False),
            dest=replace(frame.route.dest, command_or_repeated=True),
        ),
    )


def is_command(frame: "Frame") -> bool:
    """
    Determine whether the frame is a command frame.
    """
    if not (
        frame.route.dest.command_or_repeated and not frame.route.src.command_or_repeated
    ):
        return False
    return getattr(frame.control, "poll_or_final", False)


def is_response(frame: "Frame") -> bool:
    """
    Determine whether the frame is a response frame.
    """
    if not (
        frame.route.src.command_or_repeated and not frame.route.dest.command_or_repeated
    ):
        return False
    return getattr(frame.control, "poll_or_final", False)


def roll_back_ssid(address: Address) -> Address:
    """
    Given an address, return the previous SSID. This is used by nodes connecting outward
    to prevent loopback issues, by making sure that the SSID on the next connection
    outward is different from the current one, and in a way that will be inaudible by
    the time it loops back around to the original station.
    """
    ssid = address.ssid
    ssid -= 1
    if ssid < 0:
        ssid = 15
    return replace(address, ssid=ssid)
