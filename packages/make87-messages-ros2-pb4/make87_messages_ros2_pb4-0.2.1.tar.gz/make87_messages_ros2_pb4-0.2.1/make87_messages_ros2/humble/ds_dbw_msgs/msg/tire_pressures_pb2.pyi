from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TirePressures(_message.Message):
    __slots__ = ["header", "ros2_header", "front_left", "front_right", "rear_left", "rear_right", "spare"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    FRONT_LEFT_FIELD_NUMBER: _ClassVar[int]
    FRONT_RIGHT_FIELD_NUMBER: _ClassVar[int]
    REAR_LEFT_FIELD_NUMBER: _ClassVar[int]
    REAR_RIGHT_FIELD_NUMBER: _ClassVar[int]
    SPARE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    front_left: float
    front_right: float
    rear_left: float
    rear_right: float
    spare: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., front_left: _Optional[float] = ..., front_right: _Optional[float] = ..., rear_left: _Optional[float] = ..., rear_right: _Optional[float] = ..., spare: _Optional[float] = ...) -> None: ...
