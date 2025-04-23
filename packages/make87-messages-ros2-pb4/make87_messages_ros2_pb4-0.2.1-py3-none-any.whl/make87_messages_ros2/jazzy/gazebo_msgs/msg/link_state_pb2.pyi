from make87_messages_ros2.jazzy.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.jazzy.geometry_msgs.msg import twist_pb2 as _twist_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LinkState(_message.Message):
    __slots__ = ["link_name", "pose", "twist", "reference_frame"]
    LINK_NAME_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    TWIST_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_FRAME_FIELD_NUMBER: _ClassVar[int]
    link_name: str
    pose: _pose_pb2.Pose
    twist: _twist_pb2.Twist
    reference_frame: str
    def __init__(self, link_name: _Optional[str] = ..., pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., twist: _Optional[_Union[_twist_pb2.Twist, _Mapping]] = ..., reference_frame: _Optional[str] = ...) -> None: ...
