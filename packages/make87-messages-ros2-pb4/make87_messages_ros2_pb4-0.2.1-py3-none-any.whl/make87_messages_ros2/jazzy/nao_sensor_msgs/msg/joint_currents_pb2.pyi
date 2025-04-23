from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class JointCurrents(_message.Message):
    __slots__ = ["currents"]
    CURRENTS_FIELD_NUMBER: _ClassVar[int]
    currents: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, currents: _Optional[_Iterable[float]] = ...) -> None: ...
