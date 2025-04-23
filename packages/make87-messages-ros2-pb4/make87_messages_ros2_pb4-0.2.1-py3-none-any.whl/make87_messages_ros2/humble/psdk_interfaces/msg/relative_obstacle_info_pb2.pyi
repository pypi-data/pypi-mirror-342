from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RelativeObstacleInfo(_message.Message):
    __slots__ = ["header", "ros2_header", "down", "front", "right", "back", "left", "up", "down_health", "front_health", "right_health", "back_health", "left_health", "up_health", "reserved"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    DOWN_FIELD_NUMBER: _ClassVar[int]
    FRONT_FIELD_NUMBER: _ClassVar[int]
    RIGHT_FIELD_NUMBER: _ClassVar[int]
    BACK_FIELD_NUMBER: _ClassVar[int]
    LEFT_FIELD_NUMBER: _ClassVar[int]
    UP_FIELD_NUMBER: _ClassVar[int]
    DOWN_HEALTH_FIELD_NUMBER: _ClassVar[int]
    FRONT_HEALTH_FIELD_NUMBER: _ClassVar[int]
    RIGHT_HEALTH_FIELD_NUMBER: _ClassVar[int]
    BACK_HEALTH_FIELD_NUMBER: _ClassVar[int]
    LEFT_HEALTH_FIELD_NUMBER: _ClassVar[int]
    UP_HEALTH_FIELD_NUMBER: _ClassVar[int]
    RESERVED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    down: float
    front: float
    right: float
    back: float
    left: float
    up: float
    down_health: int
    front_health: int
    right_health: int
    back_health: int
    left_health: int
    up_health: int
    reserved: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., down: _Optional[float] = ..., front: _Optional[float] = ..., right: _Optional[float] = ..., back: _Optional[float] = ..., left: _Optional[float] = ..., up: _Optional[float] = ..., down_health: _Optional[int] = ..., front_health: _Optional[int] = ..., right_health: _Optional[int] = ..., back_health: _Optional[int] = ..., left_health: _Optional[int] = ..., up_health: _Optional[int] = ..., reserved: _Optional[int] = ...) -> None: ...
