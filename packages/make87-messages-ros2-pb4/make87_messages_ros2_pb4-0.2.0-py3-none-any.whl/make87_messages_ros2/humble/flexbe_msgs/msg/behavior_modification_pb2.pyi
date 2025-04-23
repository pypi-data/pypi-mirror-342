from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BehaviorModification(_message.Message):
    __slots__ = ["header", "index_begin", "index_end", "new_content"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    INDEX_BEGIN_FIELD_NUMBER: _ClassVar[int]
    INDEX_END_FIELD_NUMBER: _ClassVar[int]
    NEW_CONTENT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    index_begin: int
    index_end: int
    new_content: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., index_begin: _Optional[int] = ..., index_end: _Optional[int] = ..., new_content: _Optional[str] = ...) -> None: ...
