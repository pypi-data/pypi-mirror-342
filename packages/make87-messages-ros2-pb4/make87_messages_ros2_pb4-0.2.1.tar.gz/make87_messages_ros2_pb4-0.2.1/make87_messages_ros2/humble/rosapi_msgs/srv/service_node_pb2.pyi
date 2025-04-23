from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ServiceNodeRequest(_message.Message):
    __slots__ = ["header", "service"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    service: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., service: _Optional[str] = ...) -> None: ...

class ServiceNodeResponse(_message.Message):
    __slots__ = ["header", "node"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NODE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    node: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., node: _Optional[str] = ...) -> None: ...
