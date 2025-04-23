from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ScheduleChangeCull(_message.Message):
    __slots__ = ["time"]
    TIME_FIELD_NUMBER: _ClassVar[int]
    time: int
    def __init__(self, time: _Optional[int] = ...) -> None: ...
