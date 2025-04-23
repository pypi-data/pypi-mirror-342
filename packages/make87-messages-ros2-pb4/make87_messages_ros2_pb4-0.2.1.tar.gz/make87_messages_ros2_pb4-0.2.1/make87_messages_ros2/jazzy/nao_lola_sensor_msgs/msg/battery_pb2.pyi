from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Battery(_message.Message):
    __slots__ = ["charge", "charging", "current", "temperature"]
    CHARGE_FIELD_NUMBER: _ClassVar[int]
    CHARGING_FIELD_NUMBER: _ClassVar[int]
    CURRENT_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    charge: float
    charging: bool
    current: float
    temperature: float
    def __init__(self, charge: _Optional[float] = ..., charging: bool = ..., current: _Optional[float] = ..., temperature: _Optional[float] = ...) -> None: ...
