from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AddProblemRequest(_message.Message):
    __slots__ = ["header", "problem"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PROBLEM_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    problem: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., problem: _Optional[str] = ...) -> None: ...

class AddProblemResponse(_message.Message):
    __slots__ = ["header", "success", "error_info"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_INFO_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    error_info: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., error_info: _Optional[str] = ...) -> None: ...
