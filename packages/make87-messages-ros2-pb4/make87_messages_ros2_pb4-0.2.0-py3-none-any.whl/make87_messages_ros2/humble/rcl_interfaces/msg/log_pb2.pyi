from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Log(_message.Message):
    __slots__ = ["header", "stamp", "level", "name", "msg", "file", "function", "line"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    STAMP_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    FILE_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    LINE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    stamp: _time_pb2.Time
    level: int
    name: str
    msg: str
    file: str
    function: str
    line: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., stamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., level: _Optional[int] = ..., name: _Optional[str] = ..., msg: _Optional[str] = ..., file: _Optional[str] = ..., function: _Optional[str] = ..., line: _Optional[int] = ...) -> None: ...
