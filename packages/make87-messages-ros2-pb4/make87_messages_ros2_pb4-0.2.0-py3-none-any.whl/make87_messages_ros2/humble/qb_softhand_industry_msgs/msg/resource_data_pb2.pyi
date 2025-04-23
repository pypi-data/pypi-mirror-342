from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ResourceData(_message.Message):
    __slots__ = ["header", "name", "position", "velocity", "effort", "command"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_FIELD_NUMBER: _ClassVar[int]
    EFFORT_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    name: str
    position: float
    velocity: float
    effort: float
    command: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., name: _Optional[str] = ..., position: _Optional[float] = ..., velocity: _Optional[float] = ..., effort: _Optional[float] = ..., command: _Optional[float] = ...) -> None: ...
