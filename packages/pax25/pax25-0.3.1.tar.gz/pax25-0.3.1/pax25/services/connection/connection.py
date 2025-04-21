"""
Connections handle state and method for connections between two stations (or,
in some cases, one part of a station to another part of itself). They are
instantiated by the Frame Router, and then handed to applications for
manipulation.
"""

from dataclasses import dataclass, field, fields, replace
from enum import Enum
from typing import TYPE_CHECKING, Any, Literal, Optional, cast

from pax25.ax25.address import Address, AddressHeader, Route
from pax25.ax25.constants import AX25_PID_TEXT, AX25_SEQ_MAX, SFrameType, UCommand
from pax25.ax25.control import Info, Supervisory, Unnumbered
from pax25.ax25.frame import Frame
from pax25.ax25.matchers import (
    MatchCall,
    Matcher,
    check_all,
    has_dest_address,
    has_src_address,
    has_these_digipeaters,
    repeats_completed,
)
from pax25.ax25.utils import (
    build_receive_modifier,
    command,
    is_command,
    response,
    response_frame,
)
from pax25.services.connection.variables import FrameStateTracker
from pax25.timer import Timer, delay_action, retry_loop
from pax25.utils import EnumReprMixin, digipeater_factor

if TYPE_CHECKING:  # pragma: no cover
    from pax25.applications import BaseApplication
    from pax25.interfaces import Interface
    from pax25.services.connection.service import ConnectionService
    from pax25.station import Station


type ConnectionKey = tuple[int, int, int]


class ConnectionStatus(EnumReprMixin, Enum):
    """
    Connection status flags. The integers here match the constants direwolf uses,
    but I'm not sure that it matters so long as Python can tell them apart,
    since I don't imagine we need their values for anything in particular.
    """

    DISCONNECTED = 0
    AWAIT_CONNECTION = 1
    AWAIT_DISCONNECTION = 2
    CONNECTED = 3


class ConnectionTimeout(Exception):
    """
    Exception thrown when failing to negotiate connection.
    """


class Connection:
    """
    Connections handle state and configuration for a virtual circuit between
    stations.

    It is important to note that a connection could be loopback, which informs
    some design here.

    If sudo is True, signals to applications that this connection is safe to assume
    as a superuser if the connected name matches the station name.
    """

    def __init__(
        self,
        *,
        first_party: Address,
        second_party: Address,
        digipeaters: tuple[Address, ...],
        interface: "Interface[Any]",
        application: Optional["BaseApplication[Any]"],
        station: "Station",
        inbound: bool,
        sudo: bool = False,
        service: Optional["ConnectionService"] = None,
    ):
        # The party that initializes the connection is the first party.
        self.first_party = first_party
        # The party that receives the initial connection request is the second party.
        self.second_party = second_party
        # Only one interface per connection. If there is a bridge, it needs to be done
        # via two connections with some kind of middleware.
        self.interface = interface
        # The set of digipeaters between the first and second party. Reverse these when
        # inbound.
        self.digipeaters = digipeaters
        # Used when running the negotiation task. If we're inbound, we need to do the
        # response frame. Otherwise, we send the initial connection frame.
        self.inbound = inbound
        self.send_buffer: bytearray = bytearray()
        self.sudo = sudo
        self.application = application
        self.application_started = False
        self.service = service
        self.station = station
        self.timers = ConnectionTimers()
        self.frame_state_tracker = FrameStateTracker()
        self.status = ConnectionStatus.DISCONNECTED

    def disconnect(self) -> None:
        """
        Initializes disconnection with the remote server.
        """
        if self.status in (
            ConnectionStatus.DISCONNECTED,
            ConnectionStatus.AWAIT_DISCONNECTION,
        ):
            return
        if self.frame_state_tracker.received_without_acknowledgement:
            # Need to acknowledge outstanding frames...
            self._send_reception_status(status=SFrameType.RECEIVE_NOT_READY)
        self.status = ConnectionStatus.AWAIT_DISCONNECTION
        # ...And then immediately mark for disconnection.
        self.station.frame_router.send_frame(
            self.interface,
            command(
                Frame(
                    route=self.route_to_other(),
                    control=Unnumbered(command=UCommand.DISCONNECT),
                    pid=None,
                )
            ),
        )
        if self.application and self.application_started:
            self.application.on_disconnect(self)
        delay_action(
            timer=self.timers.t1,
            action=self._close,
            delay=digipeater_factor(
                interval=self.station.parameters["retry_interval"],
                hops=len(self.digipeaters),
            ),
        )

    def route_to_other(self) -> Route:
        """
        Route to the other station. Determines the 'other' station based on the
        'inbound' flag.
        """
        if self.inbound:
            src = self.second_party
            dest = self.first_party
            digipeaters = tuple(reversed(self.digipeaters))
        else:
            src = self.first_party
            dest = self.second_party
            digipeaters = self.digipeaters
        return Route(
            src=AddressHeader(address=src),
            dest=AddressHeader(address=dest),
            digipeaters=tuple(
                AddressHeader(address=digipeater) for digipeater in digipeaters
            ),
        )

    def _close(self) -> None:
        """
        Shuts down the attached application, performs any needed cleanup, and then
        removes this connection from the connection table, if we're associated with
        a connection service.

        If trying to close this connection from an application or service, you will want
        to use the public `disconnect` method.
        """
        if self.status == ConnectionStatus.DISCONNECTED:
            # We're already closed, nothing to do.
            return
        self.status = ConnectionStatus.DISCONNECTED
        if self.application:
            self.application.on_killed(self)
        if self.service:
            self.service.remove_connection(self)
        self.unregister()
        for field_instance in fields(self.timers):
            getattr(self.timers, field_instance.name).kill()

    def _send_accept_frame(self) -> None:
        """
        Send a connection accepted frame.
        """
        self.station.frame_router.send_frame(
            self.interface,
            response(
                Frame(
                    route=Route(
                        src=AddressHeader(address=self.second_party),
                        dest=AddressHeader(address=self.first_party),
                        digipeaters=tuple(
                            AddressHeader(address=digipeater)
                            for digipeater in reversed(self.digipeaters)
                        ),
                    ),
                    pid=None,
                    control=Unnumbered(command=UCommand.UNNUMBERED_ACKNOWLEDGE),
                )
            ),
        )

    def _send_connection_request(self) -> None:
        """
        Send a connection frame to initiate the remote connection and start listening
        for acknowledgement.
        """
        self.station.frame_router.send_frame(
            self.interface,
            command(
                Frame(
                    route=self.route_to_other(),
                    control=Unnumbered(command=UCommand.SET_ASYNC_BALANCED_MODE),
                    pid=None,
                )
            ),
        )

    def _accept_connection(self) -> None:
        """
        Update the status and send the acceptance frame.
        """
        self.status = ConnectionStatus.CONNECTED
        self._send_accept_frame()
        if self.application:
            self.application_started = True
            self.application.on_connect(self)

    @property
    def match_key(self) -> str:
        """
        Base key string used for registering/unregistering matchers.
        """
        path = Route(
            src=AddressHeader(address=self.first_party),
            dest=AddressHeader(address=self.second_party),
            digipeaters=tuple(
                AddressHeader(address=digipeater) for digipeater in self.digipeaters
            ),
        )
        return f"connection-{path}"

    @property
    def key(self) -> ConnectionKey:
        """
        Returns the connection key for this connection.
        """
        return connection_key(self.first_party, self.second_party, self.interface)

    def _handle_u_frame(self, frame: Frame) -> None:
        """
        Handle unnumbered frames.

        Some commands are not implemented because they are not part of v2.0. Some day
        we may support v2.2, but no one supports it other than Direwolf, so it's not a
        priority.

        Unnumbered Information frames are altogether ignored here. It might be possible
        to send some 'out of band' metadata with them, but this is not supported right
        now, and UI frames are not officially part of a virtual circuit.
        Other services may make use of UI, such as for APRS or similar functions.
        """
        control = cast(Unnumbered, frame.control)
        match control.command:
            case UCommand.UNNUMBERED_ACKNOWLEDGE:
                if self.status == ConnectionStatus.AWAIT_CONNECTION:
                    self.status = ConnectionStatus.CONNECTED
                    self.timers.t1.cancel()
                    if self.application:
                        self.application.on_connect(self)
                    self.send_next_frames()
                elif self.status == ConnectionStatus.AWAIT_DISCONNECTION:
                    self._close()
                # If we're not opening or closing a connection, we should ignore the
                # frame.
            case UCommand.SET_ASYNC_BALANCED_MODE:
                if self.status == ConnectionStatus.CONNECTED:
                    # Remote station must not have gotten our initial acceptance.
                    self._send_accept_frame()
            case UCommand.TEST:
                # Spec says we should echo contents of a test frame.
                frame = replace(response_frame(frame), info=frame.info)
                self.station.frame_router.send_frame(self.interface, frame)
            case UCommand.DISCONNECT:
                frame = response(
                    Frame(
                        route=self.route_to_other(),
                        control=Unnumbered(command=UCommand.UNNUMBERED_ACKNOWLEDGE),
                        pid=None,
                    )
                )
                self.station.frame_router.send_frame(self.interface, frame)
                self._close()
            case UCommand.DISCONNECT_MODE:
                # Other station seems confused we're contacting it at all, or is
                # otherwise too busy to deal with us. Close out without sending
                # acknowledgement.
                self._close()

    def _request_retransmission(self) -> None:
        """
        Requests retransmission of the frame we're next expecting.
        """
        if self.frame_state_tracker.request_retransmit:
            # We're already in the process of requesting a retransmission.
            return
        self.frame_state_tracker.request_retransmit = True
        self.station.frame_router.send_frame(
            self.interface,
            Frame(
                route=self.route_to_other(),
                control=Supervisory(
                    frame_type=SFrameType.REJECT_FRAME,
                    receiving_sequence_number=self.frame_state_tracker.vr.value,
                ),
                pid=None,
            ),
        )

    def resend_from(self, sequence_number: int) -> None:
        """
        Resend all frames starting from a given sequence number.
        """
        if self.frame_state_tracker.other_station_busy:
            return
        # Make sure these frames are resent with the current variables.
        modifier = build_receive_modifier(self.frame_state_tracker.vr.value)
        for index in self.frame_state_tracker.vs.retrace_from(sequence_number):
            frame: Frame | None = self.frame_state_tracker.outstanding_frames.get(
                index, None
            )
            if frame is None:
                # We've retraced all frames.
                return
            self.station.frame_router.send_frame(self.interface, modifier(frame))

    def _handle_s_frame(self, frame: Frame) -> None:
        """
        Handle supervisory frames.
        """
        control = cast(Supervisory, frame.control)
        match control.frame_type:
            case SFrameType.RECEIVE_READY:
                if is_command(frame):
                    self._send_reception_status(as_response=True)
                else:
                    self._clear_acknowledged_frames(control.receiving_sequence_number)
                    self.frame_state_tracker.other_station_busy = False
                    self.send_next_frames()
            case SFrameType.REJECT_FRAME:
                self._clear_acknowledged_frames(
                    control.receiving_sequence_number, retry=False
                )
                self.resend_from(control.receiving_sequence_number)
            case SFrameType.RECEIVE_NOT_READY:
                self._clear_acknowledged_frames(
                    control.receiving_sequence_number, retry=False
                )
                self.frame_state_tracker.other_station_busy = True

    def _send_reception_status(
        self,
        status: Literal[
            SFrameType.RECEIVE_READY, SFrameType.RECEIVE_NOT_READY
        ] = SFrameType.RECEIVE_READY,
        as_response: bool = False,
    ) -> None:
        """
        Sends a 'Receive Ready' or 'Receive Not Ready' frame to inform the remote
        station that we've received their frames up to a specific sequence number.
        We normally don't want to do this unless there are no I-frames we could
        shoehorn this info into.
        """
        frame = Frame(
            route=self.route_to_other(),
            control=Supervisory(
                frame_type=status,
                receiving_sequence_number=self.frame_state_tracker.vr.value,
            ),
            pid=None,
        )
        if as_response:
            frame = response(frame)
        self.station.frame_router.send_frame(
            self.interface,
            frame,
        )
        self.frame_state_tracker.received_without_acknowledgement = 0

    def _handle_i_frame(self, frame: Frame) -> None:
        """
        Handle informational frames.
        """
        control = cast(Info, frame.control)
        if self.status in (
            ConnectionStatus.AWAIT_DISCONNECTION,
            ConnectionStatus.DISCONNECTED,
        ):
            # Ignore newly sent I-frames.
            return
        if control.sending_sequence_number != self.frame_state_tracker.vr.value:
            # Don't use this frame. Instead, request retransmission from remote station.
            self._request_retransmission()
            return
        self.frame_state_tracker.request_retransmit = False
        self.frame_state_tracker.vr.increment()
        self.frame_state_tracker.received_without_acknowledgement += 1
        if self.frame_state_tracker.received_without_acknowledgement >= AX25_SEQ_MAX:
            self._send_reception_status()
        self._clear_acknowledged_frames(control.receiving_sequence_number)
        self.send_next_frames()
        self.timers.t2.cancel()
        if self.application and self.status == ConnectionStatus.CONNECTED:
            self.application.on_bytes(self, frame.info)
        delay_action(
            timer=self.timers.t2,
            action=self._send_reception_status,
            delay=500,
        )

    def _clear_acknowledged_frames(
        self, sequence_number: int, retry: bool = True
    ) -> None:
        """
        Clear all acknowledged frames from tracking, opening up slots for new
        transmitted frames.
        """
        sequence_number = self.frame_state_tracker.va.before(sequence_number)
        for i in self.frame_state_tracker.va.iterate_up_to(sequence_number):
            self.frame_state_tracker.outstanding_frames[i] = None
        if retry:
            self._retry_outstanding_loop()

    def resend_outstanding(self) -> None:
        """
        Resend all frames that have not been acknowledged.
        """
        self.resend_from(self.frame_state_tracker.va.next())

    def _retry_outstanding_loop(self) -> None:
        """
        Starts the loop for retrying any outstanding frame. Run this any time frames
        are added or the acknowledgement variable is changed.
        """
        retry_loop(
            timer=self.timers.t1,
            action=self.resend_outstanding,
            check=lambda: not any(self.frame_state_tracker.outstanding_frames.values()),
            fail_action=self.disconnect,
            immediate=False,
            retries=self.station.parameters["retries"],
            interval=digipeater_factor(
                interval=self.station.parameters["retry_interval"],
                hops=len(self.digipeaters),
            ),
        )

    def send_next_frames(self) -> None:
        """
        Sends outstanding bytes until our frame slots are consumed, or we run out of
        bytes to send.
        """
        if self.status != ConnectionStatus.CONNECTED:
            # Link is not yet ready.
            return
        if self.frame_state_tracker.other_station_busy:
            # Other station is not ready-- do not send any new information frames.
            return
        frame_sent = False
        base_frame = Frame(
            route=self.route_to_other(),
            control=Info(),
            pid=AX25_PID_TEXT,
            info=b"",
        )
        info_length = self.frame_state_tracker.maximum_transmission_unit - len(
            base_frame
        )
        assert info_length > 0, (
            "Maximum transmission unit is too small to handle even the headers!"
        )
        while (
            self.frame_state_tracker.outstanding_frames.get(
                self.frame_state_tracker.vs.value, None
            )
            is None
        ):
            # Continue sending frames until we've used up all our frame slots, or until
            # we're out of bytes to send.

            # We can cancel the Receive Ready timer since we'll send the update as part
            # of the I-frame control.
            self.timers.t2.cancel()
            byte_string = self.send_buffer[: info_length + 1]
            del self.send_buffer[: info_length + 1]
            if not byte_string:
                # We've sent everything already.
                break
            frame = replace(
                base_frame,
                control=Info(
                    receiving_sequence_number=self.frame_state_tracker.vr.value,
                    sending_sequence_number=self.frame_state_tracker.vs.value,
                ),
                info=bytes(byte_string),
            )
            self.frame_state_tracker.outstanding_frames[
                self.frame_state_tracker.vs.value
            ] = frame
            self.station.frame_router.send_frame(self.interface, frame)
            self.frame_state_tracker.vs.increment()
            self.frame_state_tracker.received_without_acknowledgement = 0
            frame_sent = True
        if frame_sent:
            self._retry_outstanding_loop()

    def send_bytes(self, bytes_to_send: bytes) -> None:
        """
        Applications can send bytes to connected clients using this function.
        """
        self.send_buffer.extend(bytes_to_send)
        self.send_next_frames()

    def inbound_frame(self, frame: Frame, _interface: "Interface") -> None:
        """
        Handles any inbound frames matching our route path.
        """
        match frame.control:
            case Unnumbered():
                self._handle_u_frame(frame)
            case Supervisory():
                self._handle_s_frame(frame)
            case Info():
                self._handle_i_frame(frame)

    def frame_matcher(self) -> Matcher:
        """
        Matches received frames.
        """
        if self.inbound:
            return check_all(
                has_src_address(self.first_party),
                has_dest_address(self.second_party),
                has_these_digipeaters(self.digipeaters),
                repeats_completed,
            )
        return check_all(
            has_src_address(self.second_party),
            has_dest_address(self.first_party),
            has_these_digipeaters(tuple(reversed(self.digipeaters))),
            repeats_completed,
        )

    def register(self) -> None:
        """
        Registers the matchers for this connection.
        """
        match_call = MatchCall(matcher=self.frame_matcher(), notify=self.inbound_frame)
        self.station.frame_router.register_matcher(
            self.match_key,
            match_call,
        )

    def unregister(self) -> None:
        """
        Unregisters the matchers for this connection.
        """
        self.station.frame_router.remove_matcher(self.match_key)

    def negotiate(self) -> None:
        """
        Performs connection negotiation, usually called after the connection object
        is initialized.
        """
        self.register()
        if self.inbound:
            self._accept_connection()
        else:
            self.status = ConnectionStatus.AWAIT_CONNECTION
            retry_loop(
                timer=self.timers.t1,
                action=self._send_connection_request,
                fail_action=self._close,
                retries=self.station.parameters["retries"],
                interval=digipeater_factor(
                    interval=self.station.parameters["retry_interval"],
                    hops=len(self.digipeaters),
                ),
            )

    def shutdown(self) -> None:
        """
        Forcibly perform connection shutdown sequence. Used by the connection service
        to close out the connection upon station shutdown. In most cases, you will want
        the .disconnect method instead to tell the other station to you intend to close.
        """
        self.disconnect()
        self._close()


def connection_key(
    party1: Address,
    party2: Address,
    interface: "Interface",
) -> ConnectionKey:
    """
    Key for use in connection tables.
    """
    return cast(
        # sorted eats the information about the number of ints in the tuple,
        # so we have to manually cast here. Please update the cast if additional
        # entries are required.
        ConnectionKey,
        tuple(sorted((hash(party1), hash(party2), hash(interface)))),
    )


@dataclass
class ConnectionTimers:
    """
    A set of timers used by a connection for various purposes.
    """

    t1: Timer = field(default_factory=lambda: Timer(name="T1[Acknowledgement]"))
    t2: Timer = field(default_factory=lambda: Timer(name="T2[Response Delay]"))
    t3: Timer = field(default_factory=lambda: Timer(name="T3[Inactive Link]"))
