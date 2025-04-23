from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SensorPerformanceMetric(_message.Message):
    __slots__ = ["name", "sim_update_rate", "real_update_rate", "fps"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SIM_UPDATE_RATE_FIELD_NUMBER: _ClassVar[int]
    REAL_UPDATE_RATE_FIELD_NUMBER: _ClassVar[int]
    FPS_FIELD_NUMBER: _ClassVar[int]
    name: str
    sim_update_rate: float
    real_update_rate: float
    fps: float
    def __init__(self, name: _Optional[str] = ..., sim_update_rate: _Optional[float] = ..., real_update_rate: _Optional[float] = ..., fps: _Optional[float] = ...) -> None: ...
