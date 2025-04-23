from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CfgVALDEL(_message.Message):
    __slots__ = ["header", "version", "layers", "reserved0", "keys"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    LAYERS_FIELD_NUMBER: _ClassVar[int]
    RESERVED0_FIELD_NUMBER: _ClassVar[int]
    KEYS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    version: int
    layers: int
    reserved0: _containers.RepeatedScalarFieldContainer[int]
    keys: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., version: _Optional[int] = ..., layers: _Optional[int] = ..., reserved0: _Optional[_Iterable[int]] = ..., keys: _Optional[_Iterable[int]] = ...) -> None: ...
