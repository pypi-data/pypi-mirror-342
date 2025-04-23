from make87_messages_ros2.rolling.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Lateral(_message.Message):
    __slots__ = ["stamp", "control_time", "steering_tire_angle", "steering_tire_rotation_rate", "is_defined_steering_tire_rotation_rate"]
    STAMP_FIELD_NUMBER: _ClassVar[int]
    CONTROL_TIME_FIELD_NUMBER: _ClassVar[int]
    STEERING_TIRE_ANGLE_FIELD_NUMBER: _ClassVar[int]
    STEERING_TIRE_ROTATION_RATE_FIELD_NUMBER: _ClassVar[int]
    IS_DEFINED_STEERING_TIRE_ROTATION_RATE_FIELD_NUMBER: _ClassVar[int]
    stamp: _time_pb2.Time
    control_time: _time_pb2.Time
    steering_tire_angle: float
    steering_tire_rotation_rate: float
    is_defined_steering_tire_rotation_rate: bool
    def __init__(self, stamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., control_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., steering_tire_angle: _Optional[float] = ..., steering_tire_rotation_rate: _Optional[float] = ..., is_defined_steering_tire_rotation_rate: bool = ...) -> None: ...
