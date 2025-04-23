from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RangeValue(_message.Message):
    __slots__ = ["min", "max", "mean"]
    MIN_FIELD_NUMBER: _ClassVar[int]
    MAX_FIELD_NUMBER: _ClassVar[int]
    MEAN_FIELD_NUMBER: _ClassVar[int]
    min: float
    max: float
    mean: float
    def __init__(self, min: _Optional[float] = ..., max: _Optional[float] = ..., mean: _Optional[float] = ...) -> None: ...
