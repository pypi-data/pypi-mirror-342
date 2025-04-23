from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Container(_message.Message):
    __slots__ = ["header", "path", "children", "outcomes", "transitions", "autonomy"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    CHILDREN_FIELD_NUMBER: _ClassVar[int]
    OUTCOMES_FIELD_NUMBER: _ClassVar[int]
    TRANSITIONS_FIELD_NUMBER: _ClassVar[int]
    AUTONOMY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    path: str
    children: _containers.RepeatedScalarFieldContainer[str]
    outcomes: _containers.RepeatedScalarFieldContainer[str]
    transitions: _containers.RepeatedScalarFieldContainer[str]
    autonomy: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., path: _Optional[str] = ..., children: _Optional[_Iterable[str]] = ..., outcomes: _Optional[_Iterable[str]] = ..., transitions: _Optional[_Iterable[str]] = ..., autonomy: _Optional[_Iterable[int]] = ...) -> None: ...
