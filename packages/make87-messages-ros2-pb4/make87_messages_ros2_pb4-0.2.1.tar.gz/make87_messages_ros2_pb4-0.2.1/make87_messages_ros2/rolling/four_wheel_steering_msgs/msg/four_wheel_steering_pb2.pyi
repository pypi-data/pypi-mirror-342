from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class FourWheelSteering(_message.Message):
    __slots__ = ["front_steering_angle", "rear_steering_angle", "front_steering_angle_velocity", "rear_steering_angle_velocity", "speed", "acceleration", "jerk"]
    FRONT_STEERING_ANGLE_FIELD_NUMBER: _ClassVar[int]
    REAR_STEERING_ANGLE_FIELD_NUMBER: _ClassVar[int]
    FRONT_STEERING_ANGLE_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    REAR_STEERING_ANGLE_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    SPEED_FIELD_NUMBER: _ClassVar[int]
    ACCELERATION_FIELD_NUMBER: _ClassVar[int]
    JERK_FIELD_NUMBER: _ClassVar[int]
    front_steering_angle: float
    rear_steering_angle: float
    front_steering_angle_velocity: float
    rear_steering_angle_velocity: float
    speed: float
    acceleration: float
    jerk: float
    def __init__(self, front_steering_angle: _Optional[float] = ..., rear_steering_angle: _Optional[float] = ..., front_steering_angle_velocity: _Optional[float] = ..., rear_steering_angle_velocity: _Optional[float] = ..., speed: _Optional[float] = ..., acceleration: _Optional[float] = ..., jerk: _Optional[float] = ...) -> None: ...
