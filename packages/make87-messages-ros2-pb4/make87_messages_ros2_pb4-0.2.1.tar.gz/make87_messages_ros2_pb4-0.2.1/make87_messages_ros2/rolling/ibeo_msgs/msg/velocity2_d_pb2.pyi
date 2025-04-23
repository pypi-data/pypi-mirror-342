from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Velocity2D(_message.Message):
    __slots__ = ["velocity_x", "velocity_y"]
    VELOCITY_X_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_Y_FIELD_NUMBER: _ClassVar[int]
    velocity_x: int
    velocity_y: int
    def __init__(self, velocity_x: _Optional[int] = ..., velocity_y: _Optional[int] = ...) -> None: ...
