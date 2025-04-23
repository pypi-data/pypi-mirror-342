from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Touch(_message.Message):
    __slots__ = ["head_front", "head_middle", "head_rear"]
    HEAD_FRONT_FIELD_NUMBER: _ClassVar[int]
    HEAD_MIDDLE_FIELD_NUMBER: _ClassVar[int]
    HEAD_REAR_FIELD_NUMBER: _ClassVar[int]
    head_front: bool
    head_middle: bool
    head_rear: bool
    def __init__(self, head_front: bool = ..., head_middle: bool = ..., head_rear: bool = ...) -> None: ...
