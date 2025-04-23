from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Sonar(_message.Message):
    __slots__ = ["left", "right"]
    LEFT_FIELD_NUMBER: _ClassVar[int]
    RIGHT_FIELD_NUMBER: _ClassVar[int]
    left: float
    right: float
    def __init__(self, left: _Optional[float] = ..., right: _Optional[float] = ...) -> None: ...
