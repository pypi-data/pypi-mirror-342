from make87_messages_ros2.rolling.geometry_msgs.msg import pose_pb2 as _pose_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SubmapEntry(_message.Message):
    __slots__ = ["trajectory_id", "submap_index", "submap_version", "pose", "is_frozen"]
    TRAJECTORY_ID_FIELD_NUMBER: _ClassVar[int]
    SUBMAP_INDEX_FIELD_NUMBER: _ClassVar[int]
    SUBMAP_VERSION_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    IS_FROZEN_FIELD_NUMBER: _ClassVar[int]
    trajectory_id: int
    submap_index: int
    submap_version: int
    pose: _pose_pb2.Pose
    is_frozen: bool
    def __init__(self, trajectory_id: _Optional[int] = ..., submap_index: _Optional[int] = ..., submap_version: _Optional[int] = ..., pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., is_frozen: bool = ...) -> None: ...
