from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class NegotiationNotice(_message.Message):
    __slots__ = ["conflict_version", "participants"]
    CONFLICT_VERSION_FIELD_NUMBER: _ClassVar[int]
    PARTICIPANTS_FIELD_NUMBER: _ClassVar[int]
    conflict_version: int
    participants: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, conflict_version: _Optional[int] = ..., participants: _Optional[_Iterable[int]] = ...) -> None: ...
