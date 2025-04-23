from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.moveit_msgs.msg import planning_scene_pb2 as _planning_scene_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ApplyPlanningSceneRequest(_message.Message):
    __slots__ = ["header", "scene"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SCENE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    scene: _planning_scene_pb2.PlanningScene
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., scene: _Optional[_Union[_planning_scene_pb2.PlanningScene, _Mapping]] = ...) -> None: ...

class ApplyPlanningSceneResponse(_message.Message):
    __slots__ = ["header", "success"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ...) -> None: ...
