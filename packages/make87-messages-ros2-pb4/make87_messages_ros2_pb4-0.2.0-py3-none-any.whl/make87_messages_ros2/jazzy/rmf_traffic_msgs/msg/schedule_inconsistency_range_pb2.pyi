from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ScheduleInconsistencyRange(_message.Message):
    __slots__ = ["lower", "upper"]
    LOWER_FIELD_NUMBER: _ClassVar[int]
    UPPER_FIELD_NUMBER: _ClassVar[int]
    lower: int
    upper: int
    def __init__(self, lower: _Optional[int] = ..., upper: _Optional[int] = ...) -> None: ...
