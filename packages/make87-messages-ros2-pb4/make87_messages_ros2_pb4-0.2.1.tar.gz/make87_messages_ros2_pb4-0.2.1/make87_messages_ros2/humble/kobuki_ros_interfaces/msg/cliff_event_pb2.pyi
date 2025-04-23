from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CliffEvent(_message.Message):
    __slots__ = ["header", "sensor", "state", "bottom"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SENSOR_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    BOTTOM_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    sensor: int
    state: int
    bottom: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., sensor: _Optional[int] = ..., state: _Optional[int] = ..., bottom: _Optional[int] = ...) -> None: ...
