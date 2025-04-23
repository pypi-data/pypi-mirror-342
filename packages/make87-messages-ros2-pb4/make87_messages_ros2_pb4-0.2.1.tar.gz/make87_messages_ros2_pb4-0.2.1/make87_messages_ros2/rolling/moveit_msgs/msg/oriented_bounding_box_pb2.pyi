from make87_messages_ros2.rolling.geometry_msgs.msg import point32_pb2 as _point32_pb2
from make87_messages_ros2.rolling.geometry_msgs.msg import pose_pb2 as _pose_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OrientedBoundingBox(_message.Message):
    __slots__ = ["pose", "extents"]
    POSE_FIELD_NUMBER: _ClassVar[int]
    EXTENTS_FIELD_NUMBER: _ClassVar[int]
    pose: _pose_pb2.Pose
    extents: _point32_pb2.Point32
    def __init__(self, pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., extents: _Optional[_Union[_point32_pb2.Point32, _Mapping]] = ...) -> None: ...
