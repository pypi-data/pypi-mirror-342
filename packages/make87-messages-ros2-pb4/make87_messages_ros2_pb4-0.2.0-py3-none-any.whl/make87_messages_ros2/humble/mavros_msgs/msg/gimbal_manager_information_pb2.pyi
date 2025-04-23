from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GimbalManagerInformation(_message.Message):
    __slots__ = ["header", "ros2_header", "cap_flags", "gimbal_device_id", "roll_min", "roll_max", "pitch_min", "pitch_max", "yaw_min", "yaw_max"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    CAP_FLAGS_FIELD_NUMBER: _ClassVar[int]
    GIMBAL_DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    ROLL_MIN_FIELD_NUMBER: _ClassVar[int]
    ROLL_MAX_FIELD_NUMBER: _ClassVar[int]
    PITCH_MIN_FIELD_NUMBER: _ClassVar[int]
    PITCH_MAX_FIELD_NUMBER: _ClassVar[int]
    YAW_MIN_FIELD_NUMBER: _ClassVar[int]
    YAW_MAX_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    cap_flags: int
    gimbal_device_id: int
    roll_min: float
    roll_max: float
    pitch_min: float
    pitch_max: float
    yaw_min: float
    yaw_max: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., cap_flags: _Optional[int] = ..., gimbal_device_id: _Optional[int] = ..., roll_min: _Optional[float] = ..., roll_max: _Optional[float] = ..., pitch_min: _Optional[float] = ..., pitch_max: _Optional[float] = ..., yaw_min: _Optional[float] = ..., yaw_max: _Optional[float] = ...) -> None: ...
