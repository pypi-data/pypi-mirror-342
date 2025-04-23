from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Size2D(_message.Message):
    __slots__ = ["size_x", "size_y"]
    SIZE_X_FIELD_NUMBER: _ClassVar[int]
    SIZE_Y_FIELD_NUMBER: _ClassVar[int]
    size_x: int
    size_y: int
    def __init__(self, size_x: _Optional[int] = ..., size_y: _Optional[int] = ...) -> None: ...
