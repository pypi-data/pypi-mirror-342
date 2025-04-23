from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.vision_msgs.msg import pose2_d_pb2 as _pose2_d_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BoundingBox2D(_message.Message):
    __slots__ = ["header", "center", "size_x", "size_y"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CENTER_FIELD_NUMBER: _ClassVar[int]
    SIZE_X_FIELD_NUMBER: _ClassVar[int]
    SIZE_Y_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    center: _pose2_d_pb2.Pose2D
    size_x: float
    size_y: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., center: _Optional[_Union[_pose2_d_pb2.Pose2D, _Mapping]] = ..., size_x: _Optional[float] = ..., size_y: _Optional[float] = ...) -> None: ...
