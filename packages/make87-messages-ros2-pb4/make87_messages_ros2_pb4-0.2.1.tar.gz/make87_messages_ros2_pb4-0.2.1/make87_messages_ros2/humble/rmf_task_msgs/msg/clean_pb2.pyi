from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Clean(_message.Message):
    __slots__ = ["header", "start_waypoint"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    START_WAYPOINT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    start_waypoint: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., start_waypoint: _Optional[str] = ...) -> None: ...
