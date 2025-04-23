from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TF2Error(_message.Message):
    __slots__ = ["header", "error", "error_string"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    ERROR_STRING_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    error: int
    error_string: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., error: _Optional[int] = ..., error_string: _Optional[str] = ...) -> None: ...
