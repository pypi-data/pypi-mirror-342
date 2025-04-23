from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CfgRATE(_message.Message):
    __slots__ = ["meas_rate", "nav_rate", "time_ref"]
    MEAS_RATE_FIELD_NUMBER: _ClassVar[int]
    NAV_RATE_FIELD_NUMBER: _ClassVar[int]
    TIME_REF_FIELD_NUMBER: _ClassVar[int]
    meas_rate: int
    nav_rate: int
    time_ref: int
    def __init__(self, meas_rate: _Optional[int] = ..., nav_rate: _Optional[int] = ..., time_ref: _Optional[int] = ...) -> None: ...
