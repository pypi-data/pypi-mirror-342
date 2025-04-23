from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose2_d_pb2 as _pose2_d_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NormalizedImageCropRequest(_message.Message):
    __slots__ = ["header", "top_left", "bottom_right"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TOP_LEFT_FIELD_NUMBER: _ClassVar[int]
    BOTTOM_RIGHT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    top_left: _pose2_d_pb2.Pose2D
    bottom_right: _pose2_d_pb2.Pose2D
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., top_left: _Optional[_Union[_pose2_d_pb2.Pose2D, _Mapping]] = ..., bottom_right: _Optional[_Union[_pose2_d_pb2.Pose2D, _Mapping]] = ...) -> None: ...

class NormalizedImageCropResponse(_message.Message):
    __slots__ = ["header", "status"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    status: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., status: _Optional[int] = ...) -> None: ...
