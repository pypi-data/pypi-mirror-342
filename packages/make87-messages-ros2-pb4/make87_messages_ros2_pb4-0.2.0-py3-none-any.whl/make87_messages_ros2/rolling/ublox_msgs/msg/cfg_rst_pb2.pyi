from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CfgRST(_message.Message):
    __slots__ = ["nav_bbr_mask", "reset_mode", "reserved1"]
    NAV_BBR_MASK_FIELD_NUMBER: _ClassVar[int]
    RESET_MODE_FIELD_NUMBER: _ClassVar[int]
    RESERVED1_FIELD_NUMBER: _ClassVar[int]
    nav_bbr_mask: int
    reset_mode: int
    reserved1: int
    def __init__(self, nav_bbr_mask: _Optional[int] = ..., reset_mode: _Optional[int] = ..., reserved1: _Optional[int] = ...) -> None: ...
