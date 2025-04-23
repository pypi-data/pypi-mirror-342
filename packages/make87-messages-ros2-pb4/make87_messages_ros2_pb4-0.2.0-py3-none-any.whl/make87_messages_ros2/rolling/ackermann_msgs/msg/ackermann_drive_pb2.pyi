from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AckermannDrive(_message.Message):
    __slots__ = ["steering_angle", "steering_angle_velocity", "speed", "acceleration", "jerk"]
    STEERING_ANGLE_FIELD_NUMBER: _ClassVar[int]
    STEERING_ANGLE_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    SPEED_FIELD_NUMBER: _ClassVar[int]
    ACCELERATION_FIELD_NUMBER: _ClassVar[int]
    JERK_FIELD_NUMBER: _ClassVar[int]
    steering_angle: float
    steering_angle_velocity: float
    speed: float
    acceleration: float
    jerk: float
    def __init__(self, steering_angle: _Optional[float] = ..., steering_angle_velocity: _Optional[float] = ..., speed: _Optional[float] = ..., acceleration: _Optional[float] = ..., jerk: _Optional[float] = ...) -> None: ...
