from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.hri_msgs.msg import normalized_point_of_interest2_d_pb2 as _normalized_point_of_interest2_d_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FacialLandmarks(_message.Message):
    __slots__ = ["header", "ros2_header", "landmarks", "height", "width"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    LANDMARKS_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    landmarks: _containers.RepeatedCompositeFieldContainer[_normalized_point_of_interest2_d_pb2.NormalizedPointOfInterest2D]
    height: int
    width: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., landmarks: _Optional[_Iterable[_Union[_normalized_point_of_interest2_d_pb2.NormalizedPointOfInterest2D, _Mapping]]] = ..., height: _Optional[int] = ..., width: _Optional[int] = ...) -> None: ...
