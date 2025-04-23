from make87_messages_ros2.rolling.autoware_planning_msgs.msg import lanelet_segment_pb2 as _lanelet_segment_pb2
from make87_messages_ros2.rolling.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from make87_messages_ros2.rolling.unique_identifier_msgs.msg import uuid_pb2 as _uuid_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LaneletRoute(_message.Message):
    __slots__ = ["header", "start_pose", "goal_pose", "segments", "uuid", "allow_modification"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    START_POSE_FIELD_NUMBER: _ClassVar[int]
    GOAL_POSE_FIELD_NUMBER: _ClassVar[int]
    SEGMENTS_FIELD_NUMBER: _ClassVar[int]
    UUID_FIELD_NUMBER: _ClassVar[int]
    ALLOW_MODIFICATION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    start_pose: _pose_pb2.Pose
    goal_pose: _pose_pb2.Pose
    segments: _containers.RepeatedCompositeFieldContainer[_lanelet_segment_pb2.LaneletSegment]
    uuid: _uuid_pb2.UUID
    allow_modification: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., start_pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., goal_pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., segments: _Optional[_Iterable[_Union[_lanelet_segment_pb2.LaneletSegment, _Mapping]]] = ..., uuid: _Optional[_Union[_uuid_pb2.UUID, _Mapping]] = ..., allow_modification: bool = ...) -> None: ...
