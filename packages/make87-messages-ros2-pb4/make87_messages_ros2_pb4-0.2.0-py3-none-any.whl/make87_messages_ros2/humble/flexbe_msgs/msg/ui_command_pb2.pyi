from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UICommand(_message.Message):
    __slots__ = ["header", "command", "key"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    command: str
    key: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., command: _Optional[str] = ..., key: _Optional[str] = ...) -> None: ...
