from make87_messages_ros2.jazzy.geometry_msgs.msg import pose_pb2 as _pose_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Particle(_message.Message):
    __slots__ = ["pose", "weight"]
    POSE_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_FIELD_NUMBER: _ClassVar[int]
    pose: _pose_pb2.Pose
    weight: float
    def __init__(self, pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., weight: _Optional[float] = ...) -> None: ...
