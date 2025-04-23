from make87_messages_ros2.jazzy.moveit_msgs.msg import planning_scene_pb2 as _planning_scene_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ApplyPlanningSceneRequest(_message.Message):
    __slots__ = ["scene"]
    SCENE_FIELD_NUMBER: _ClassVar[int]
    scene: _planning_scene_pb2.PlanningScene
    def __init__(self, scene: _Optional[_Union[_planning_scene_pb2.PlanningScene, _Mapping]] = ...) -> None: ...

class ApplyPlanningSceneResponse(_message.Message):
    __slots__ = ["success"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
