from make87_messages_ros2.rolling.actuator_msgs.msg import actuators_angular_velocity_pb2 as _actuators_angular_velocity_pb2
from make87_messages_ros2.rolling.actuator_msgs.msg import actuators_linear_velocity_pb2 as _actuators_linear_velocity_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ActuatorsVelocity(_message.Message):
    __slots__ = ["header", "angular", "linear"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ANGULAR_FIELD_NUMBER: _ClassVar[int]
    LINEAR_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    angular: _actuators_angular_velocity_pb2.ActuatorsAngularVelocity
    linear: _actuators_linear_velocity_pb2.ActuatorsLinearVelocity
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., angular: _Optional[_Union[_actuators_angular_velocity_pb2.ActuatorsAngularVelocity, _Mapping]] = ..., linear: _Optional[_Union[_actuators_linear_velocity_pb2.ActuatorsLinearVelocity, _Mapping]] = ...) -> None: ...
