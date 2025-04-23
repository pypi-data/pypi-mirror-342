from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class MissionRemainingDistanceTime(_message.Message):
    __slots__ = ["remaining_distance", "remaining_time"]
    REMAINING_DISTANCE_FIELD_NUMBER: _ClassVar[int]
    REMAINING_TIME_FIELD_NUMBER: _ClassVar[int]
    remaining_distance: float
    remaining_time: float
    def __init__(self, remaining_distance: _Optional[float] = ..., remaining_time: _Optional[float] = ...) -> None: ...
