from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.humble.ros_gz_interfaces.msg import entity_pb2 as _entity_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetEntityPoseRequest(_message.Message):
    __slots__ = ["header", "entity", "pose"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    entity: _entity_pb2.Entity
    pose: _pose_pb2.Pose
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., entity: _Optional[_Union[_entity_pb2.Entity, _Mapping]] = ..., pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ...) -> None: ...

class SetEntityPoseResponse(_message.Message):
    __slots__ = ["header", "success"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ...) -> None: ...
