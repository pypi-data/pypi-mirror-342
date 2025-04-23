from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class WheelStates(_message.Message):
    __slots__ = ["header", "stamp", "position", "velocity", "torque", "pwm_duty_cycle"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    STAMP_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_FIELD_NUMBER: _ClassVar[int]
    TORQUE_FIELD_NUMBER: _ClassVar[int]
    PWM_DUTY_CYCLE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    stamp: _time_pb2.Time
    position: _containers.RepeatedScalarFieldContainer[float]
    velocity: _containers.RepeatedScalarFieldContainer[float]
    torque: _containers.RepeatedScalarFieldContainer[float]
    pwm_duty_cycle: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., stamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., position: _Optional[_Iterable[float]] = ..., velocity: _Optional[_Iterable[float]] = ..., torque: _Optional[_Iterable[float]] = ..., pwm_duty_cycle: _Optional[_Iterable[float]] = ...) -> None: ...
