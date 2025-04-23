from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetMeasurementsRequest(_message.Message):
    __slots__ = ["header", "id", "max_repeats", "get_positions", "get_currents", "get_commands"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    MAX_REPEATS_FIELD_NUMBER: _ClassVar[int]
    GET_POSITIONS_FIELD_NUMBER: _ClassVar[int]
    GET_CURRENTS_FIELD_NUMBER: _ClassVar[int]
    GET_COMMANDS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    id: int
    max_repeats: int
    get_positions: bool
    get_currents: bool
    get_commands: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., id: _Optional[int] = ..., max_repeats: _Optional[int] = ..., get_positions: bool = ..., get_currents: bool = ..., get_commands: bool = ...) -> None: ...

class GetMeasurementsResponse(_message.Message):
    __slots__ = ["header", "success", "failures", "positions", "currents", "commands", "stamp"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    FAILURES_FIELD_NUMBER: _ClassVar[int]
    POSITIONS_FIELD_NUMBER: _ClassVar[int]
    CURRENTS_FIELD_NUMBER: _ClassVar[int]
    COMMANDS_FIELD_NUMBER: _ClassVar[int]
    STAMP_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    failures: int
    positions: _containers.RepeatedScalarFieldContainer[int]
    currents: _containers.RepeatedScalarFieldContainer[int]
    commands: _containers.RepeatedScalarFieldContainer[int]
    stamp: _time_pb2.Time
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., failures: _Optional[int] = ..., positions: _Optional[_Iterable[int]] = ..., currents: _Optional[_Iterable[int]] = ..., commands: _Optional[_Iterable[int]] = ..., stamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ...) -> None: ...
