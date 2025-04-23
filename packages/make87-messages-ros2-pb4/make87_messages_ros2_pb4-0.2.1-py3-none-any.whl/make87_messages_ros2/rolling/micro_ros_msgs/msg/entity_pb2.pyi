from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Entity(_message.Message):
    __slots__ = ["entity_type", "name", "types"]
    ENTITY_TYPE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPES_FIELD_NUMBER: _ClassVar[int]
    entity_type: int
    name: str
    types: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, entity_type: _Optional[int] = ..., name: _Optional[str] = ..., types: _Optional[_Iterable[str]] = ...) -> None: ...
