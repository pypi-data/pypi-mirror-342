from make87_messages_ros2.rolling.rmf_reservation_msgs.msg import ticket_pb2 as _ticket_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ClaimRequest(_message.Message):
    __slots__ = ["ticket", "wait_points"]
    TICKET_FIELD_NUMBER: _ClassVar[int]
    WAIT_POINTS_FIELD_NUMBER: _ClassVar[int]
    ticket: _ticket_pb2.Ticket
    wait_points: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, ticket: _Optional[_Union[_ticket_pb2.Ticket, _Mapping]] = ..., wait_points: _Optional[_Iterable[str]] = ...) -> None: ...
