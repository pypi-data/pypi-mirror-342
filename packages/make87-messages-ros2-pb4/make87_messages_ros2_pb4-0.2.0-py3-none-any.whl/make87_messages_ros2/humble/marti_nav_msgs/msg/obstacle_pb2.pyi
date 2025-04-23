from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import point_pb2 as _point_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_pb2 as _pose_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Obstacle(_message.Message):
    __slots__ = ["header", "id", "pose", "polygon"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    POLYGON_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    id: str
    pose: _pose_pb2.Pose
    polygon: _containers.RepeatedCompositeFieldContainer[_point_pb2.Point]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., id: _Optional[str] = ..., pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., polygon: _Optional[_Iterable[_Union[_point_pb2.Point, _Mapping]]] = ...) -> None: ...
