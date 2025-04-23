from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ListControllerTypesRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ListControllerTypesResponse(_message.Message):
    __slots__ = ["types", "base_classes"]
    TYPES_FIELD_NUMBER: _ClassVar[int]
    BASE_CLASSES_FIELD_NUMBER: _ClassVar[int]
    types: _containers.RepeatedScalarFieldContainer[str]
    base_classes: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, types: _Optional[_Iterable[str]] = ..., base_classes: _Optional[_Iterable[str]] = ...) -> None: ...
