from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Info(_message.Message):
    __slots__ = ["header", "id", "serial_port", "max_repeats", "get_positions", "get_currents", "get_distinct_packages", "set_commands", "set_commands_async", "position_limits", "encoder_resolutions"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    SERIAL_PORT_FIELD_NUMBER: _ClassVar[int]
    MAX_REPEATS_FIELD_NUMBER: _ClassVar[int]
    GET_POSITIONS_FIELD_NUMBER: _ClassVar[int]
    GET_CURRENTS_FIELD_NUMBER: _ClassVar[int]
    GET_DISTINCT_PACKAGES_FIELD_NUMBER: _ClassVar[int]
    SET_COMMANDS_FIELD_NUMBER: _ClassVar[int]
    SET_COMMANDS_ASYNC_FIELD_NUMBER: _ClassVar[int]
    POSITION_LIMITS_FIELD_NUMBER: _ClassVar[int]
    ENCODER_RESOLUTIONS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    id: int
    serial_port: str
    max_repeats: int
    get_positions: bool
    get_currents: bool
    get_distinct_packages: bool
    set_commands: bool
    set_commands_async: bool
    position_limits: _containers.RepeatedScalarFieldContainer[int]
    encoder_resolutions: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., id: _Optional[int] = ..., serial_port: _Optional[str] = ..., max_repeats: _Optional[int] = ..., get_positions: bool = ..., get_currents: bool = ..., get_distinct_packages: bool = ..., set_commands: bool = ..., set_commands_async: bool = ..., position_limits: _Optional[_Iterable[int]] = ..., encoder_resolutions: _Optional[_Iterable[int]] = ...) -> None: ...
