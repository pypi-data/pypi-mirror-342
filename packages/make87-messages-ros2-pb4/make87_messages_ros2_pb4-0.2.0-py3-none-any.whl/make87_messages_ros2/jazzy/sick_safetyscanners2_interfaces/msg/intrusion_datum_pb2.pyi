from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class IntrusionDatum(_message.Message):
    __slots__ = ["size", "flags"]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    size: int
    flags: _containers.RepeatedScalarFieldContainer[bool]
    def __init__(self, size: _Optional[int] = ..., flags: _Optional[_Iterable[bool]] = ...) -> None: ...
