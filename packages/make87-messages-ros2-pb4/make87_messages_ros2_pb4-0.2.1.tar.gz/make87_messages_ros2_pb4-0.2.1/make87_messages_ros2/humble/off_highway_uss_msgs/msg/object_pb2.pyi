from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import point_pb2 as _point_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Object(_message.Message):
    __slots__ = ["header", "ros2_header", "id", "position_first", "exist_probability", "position_second", "object_type"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIRST_FIELD_NUMBER: _ClassVar[int]
    EXIST_PROBABILITY_FIELD_NUMBER: _ClassVar[int]
    POSITION_SECOND_FIELD_NUMBER: _ClassVar[int]
    OBJECT_TYPE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    id: int
    position_first: _point_pb2.Point
    exist_probability: float
    position_second: _point_pb2.Point
    object_type: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., id: _Optional[int] = ..., position_first: _Optional[_Union[_point_pb2.Point, _Mapping]] = ..., exist_probability: _Optional[float] = ..., position_second: _Optional[_Union[_point_pb2.Point, _Mapping]] = ..., object_type: _Optional[int] = ...) -> None: ...
