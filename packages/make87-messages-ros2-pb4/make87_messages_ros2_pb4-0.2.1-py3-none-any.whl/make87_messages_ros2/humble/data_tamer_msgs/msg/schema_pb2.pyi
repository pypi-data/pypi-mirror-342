from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Schema(_message.Message):
    __slots__ = ["header", "hash", "channel_name", "schema_text"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_NAME_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_TEXT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    hash: int
    channel_name: str
    schema_text: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., hash: _Optional[int] = ..., channel_name: _Optional[str] = ..., schema_text: _Optional[str] = ...) -> None: ...
