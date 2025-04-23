from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LoadRequest(_message.Message):
    __slots__ = ["header", "filename"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FILENAME_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    filename: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., filename: _Optional[str] = ...) -> None: ...

class LoadResponse(_message.Message):
    __slots__ = ["header", "answer", "success"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ANSWER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    answer: str
    success: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., answer: _Optional[str] = ..., success: bool = ...) -> None: ...
