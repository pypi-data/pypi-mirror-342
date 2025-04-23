from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SbgUtcTimeStatus(_message.Message):
    __slots__ = ["clock_stable", "clock_status", "clock_utc_sync", "clock_utc_status"]
    CLOCK_STABLE_FIELD_NUMBER: _ClassVar[int]
    CLOCK_STATUS_FIELD_NUMBER: _ClassVar[int]
    CLOCK_UTC_SYNC_FIELD_NUMBER: _ClassVar[int]
    CLOCK_UTC_STATUS_FIELD_NUMBER: _ClassVar[int]
    clock_stable: bool
    clock_status: int
    clock_utc_sync: bool
    clock_utc_status: int
    def __init__(self, clock_stable: bool = ..., clock_status: _Optional[int] = ..., clock_utc_sync: bool = ..., clock_utc_status: _Optional[int] = ...) -> None: ...
