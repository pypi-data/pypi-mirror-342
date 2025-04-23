from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_pb2 as _pose_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GridMapInfo(_message.Message):
    __slots__ = ["header", "resolution", "length_x", "length_y", "pose"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    RESOLUTION_FIELD_NUMBER: _ClassVar[int]
    LENGTH_X_FIELD_NUMBER: _ClassVar[int]
    LENGTH_Y_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    resolution: float
    length_x: float
    length_y: float
    pose: _pose_pb2.Pose
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., resolution: _Optional[float] = ..., length_x: _Optional[float] = ..., length_y: _Optional[float] = ..., pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ...) -> None: ...
