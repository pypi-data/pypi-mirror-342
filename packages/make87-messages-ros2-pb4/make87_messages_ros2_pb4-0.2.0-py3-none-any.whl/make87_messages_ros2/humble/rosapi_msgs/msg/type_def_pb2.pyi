from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TypeDef(_message.Message):
    __slots__ = ["header", "type", "fieldnames", "fieldtypes", "fieldarraylen", "examples", "constnames", "constvalues"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    FIELDNAMES_FIELD_NUMBER: _ClassVar[int]
    FIELDTYPES_FIELD_NUMBER: _ClassVar[int]
    FIELDARRAYLEN_FIELD_NUMBER: _ClassVar[int]
    EXAMPLES_FIELD_NUMBER: _ClassVar[int]
    CONSTNAMES_FIELD_NUMBER: _ClassVar[int]
    CONSTVALUES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    type: str
    fieldnames: _containers.RepeatedScalarFieldContainer[str]
    fieldtypes: _containers.RepeatedScalarFieldContainer[str]
    fieldarraylen: _containers.RepeatedScalarFieldContainer[int]
    examples: _containers.RepeatedScalarFieldContainer[str]
    constnames: _containers.RepeatedScalarFieldContainer[str]
    constvalues: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., type: _Optional[str] = ..., fieldnames: _Optional[_Iterable[str]] = ..., fieldtypes: _Optional[_Iterable[str]] = ..., fieldarraylen: _Optional[_Iterable[int]] = ..., examples: _Optional[_Iterable[str]] = ..., constnames: _Optional[_Iterable[str]] = ..., constvalues: _Optional[_Iterable[str]] = ...) -> None: ...
