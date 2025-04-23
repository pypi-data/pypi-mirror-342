from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NegotiationStatus(_message.Message):
    __slots__ = ["header", "conflict_version", "participants", "start_time", "last_response_time"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CONFLICT_VERSION_FIELD_NUMBER: _ClassVar[int]
    PARTICIPANTS_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    LAST_RESPONSE_TIME_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    conflict_version: int
    participants: _containers.RepeatedScalarFieldContainer[int]
    start_time: _time_pb2.Time
    last_response_time: _time_pb2.Time
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., conflict_version: _Optional[int] = ..., participants: _Optional[_Iterable[int]] = ..., start_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., last_response_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ...) -> None: ...
