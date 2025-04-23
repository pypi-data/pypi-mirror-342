from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ActuatorsLinearVelocity(_message.Message):
    __slots__ = ["velocity"]
    VELOCITY_FIELD_NUMBER: _ClassVar[int]
    velocity: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, velocity: _Optional[_Iterable[float]] = ...) -> None: ...
