from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SbgShipMotionStatus(_message.Message):
    __slots__ = ["heave_valid", "heave_vel_aided", "surge_sway_included", "period_available", "period_valid", "swell_mode"]
    HEAVE_VALID_FIELD_NUMBER: _ClassVar[int]
    HEAVE_VEL_AIDED_FIELD_NUMBER: _ClassVar[int]
    SURGE_SWAY_INCLUDED_FIELD_NUMBER: _ClassVar[int]
    PERIOD_AVAILABLE_FIELD_NUMBER: _ClassVar[int]
    PERIOD_VALID_FIELD_NUMBER: _ClassVar[int]
    SWELL_MODE_FIELD_NUMBER: _ClassVar[int]
    heave_valid: bool
    heave_vel_aided: bool
    surge_sway_included: bool
    period_available: bool
    period_valid: bool
    swell_mode: bool
    def __init__(self, heave_valid: bool = ..., heave_vel_aided: bool = ..., surge_sway_included: bool = ..., period_available: bool = ..., period_valid: bool = ..., swell_mode: bool = ...) -> None: ...
