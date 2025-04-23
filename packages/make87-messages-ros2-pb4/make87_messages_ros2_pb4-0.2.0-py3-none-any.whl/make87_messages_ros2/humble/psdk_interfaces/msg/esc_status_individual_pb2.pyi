from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EscStatusIndividual(_message.Message):
    __slots__ = ["header", "current", "speed", "voltage", "temperature", "stall", "empty", "unbalanced", "esc_disconnected", "temperature_high"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CURRENT_FIELD_NUMBER: _ClassVar[int]
    SPEED_FIELD_NUMBER: _ClassVar[int]
    VOLTAGE_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    STALL_FIELD_NUMBER: _ClassVar[int]
    EMPTY_FIELD_NUMBER: _ClassVar[int]
    UNBALANCED_FIELD_NUMBER: _ClassVar[int]
    ESC_DISCONNECTED_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_HIGH_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    current: int
    speed: int
    voltage: int
    temperature: int
    stall: int
    empty: int
    unbalanced: int
    esc_disconnected: int
    temperature_high: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., current: _Optional[int] = ..., speed: _Optional[int] = ..., voltage: _Optional[int] = ..., temperature: _Optional[int] = ..., stall: _Optional[int] = ..., empty: _Optional[int] = ..., unbalanced: _Optional[int] = ..., esc_disconnected: _Optional[int] = ..., temperature_high: _Optional[int] = ...) -> None: ...
