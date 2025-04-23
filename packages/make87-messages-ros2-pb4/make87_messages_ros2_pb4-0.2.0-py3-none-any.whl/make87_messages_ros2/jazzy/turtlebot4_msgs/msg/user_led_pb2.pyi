from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class UserLed(_message.Message):
    __slots__ = ["led", "color", "blink_period", "duty_cycle"]
    LED_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    BLINK_PERIOD_FIELD_NUMBER: _ClassVar[int]
    DUTY_CYCLE_FIELD_NUMBER: _ClassVar[int]
    led: int
    color: int
    blink_period: int
    duty_cycle: float
    def __init__(self, led: _Optional[int] = ..., color: _Optional[int] = ..., blink_period: _Optional[int] = ..., duty_cycle: _Optional[float] = ...) -> None: ...
