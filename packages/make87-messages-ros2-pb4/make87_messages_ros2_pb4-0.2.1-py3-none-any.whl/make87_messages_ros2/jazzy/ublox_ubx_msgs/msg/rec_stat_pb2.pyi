from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RecStat(_message.Message):
    __slots__ = ["leap_sec", "clk_reset"]
    LEAP_SEC_FIELD_NUMBER: _ClassVar[int]
    CLK_RESET_FIELD_NUMBER: _ClassVar[int]
    leap_sec: bool
    clk_reset: bool
    def __init__(self, leap_sec: bool = ..., clk_reset: bool = ...) -> None: ...
