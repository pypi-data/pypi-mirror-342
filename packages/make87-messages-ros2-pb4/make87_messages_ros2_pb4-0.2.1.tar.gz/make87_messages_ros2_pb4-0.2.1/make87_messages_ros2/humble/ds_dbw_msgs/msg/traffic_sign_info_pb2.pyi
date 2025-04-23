from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TrafficSignInfo(_message.Message):
    __slots__ = ["header", "ros2_header", "status", "camera_used", "navigation_used", "speed_units", "speed_limit"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CAMERA_USED_FIELD_NUMBER: _ClassVar[int]
    NAVIGATION_USED_FIELD_NUMBER: _ClassVar[int]
    SPEED_UNITS_FIELD_NUMBER: _ClassVar[int]
    SPEED_LIMIT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    status: int
    camera_used: bool
    navigation_used: bool
    speed_units: int
    speed_limit: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., status: _Optional[int] = ..., camera_used: bool = ..., navigation_used: bool = ..., speed_units: _Optional[int] = ..., speed_limit: _Optional[float] = ...) -> None: ...
