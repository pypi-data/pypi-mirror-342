from make87_messages_ros2.jazzy.moveit_msgs.msg import collision_object_pb2 as _collision_object_pb2
from make87_messages_ros2.jazzy.moveit_msgs.msg import grasp_pb2 as _grasp_pb2
from make87_messages_ros2.jazzy.moveit_msgs.msg import move_it_error_codes_pb2 as _move_it_error_codes_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GraspPlanningRequest(_message.Message):
    __slots__ = ["group_name", "target", "support_surfaces", "candidate_grasps", "movable_obstacles"]
    GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_SURFACES_FIELD_NUMBER: _ClassVar[int]
    CANDIDATE_GRASPS_FIELD_NUMBER: _ClassVar[int]
    MOVABLE_OBSTACLES_FIELD_NUMBER: _ClassVar[int]
    group_name: str
    target: _collision_object_pb2.CollisionObject
    support_surfaces: _containers.RepeatedScalarFieldContainer[str]
    candidate_grasps: _containers.RepeatedCompositeFieldContainer[_grasp_pb2.Grasp]
    movable_obstacles: _containers.RepeatedCompositeFieldContainer[_collision_object_pb2.CollisionObject]
    def __init__(self, group_name: _Optional[str] = ..., target: _Optional[_Union[_collision_object_pb2.CollisionObject, _Mapping]] = ..., support_surfaces: _Optional[_Iterable[str]] = ..., candidate_grasps: _Optional[_Iterable[_Union[_grasp_pb2.Grasp, _Mapping]]] = ..., movable_obstacles: _Optional[_Iterable[_Union[_collision_object_pb2.CollisionObject, _Mapping]]] = ...) -> None: ...

class GraspPlanningResponse(_message.Message):
    __slots__ = ["grasps", "error_code"]
    GRASPS_FIELD_NUMBER: _ClassVar[int]
    ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    grasps: _containers.RepeatedCompositeFieldContainer[_grasp_pb2.Grasp]
    error_code: _move_it_error_codes_pb2.MoveItErrorCodes
    def __init__(self, grasps: _Optional[_Iterable[_Union[_grasp_pb2.Grasp, _Mapping]]] = ..., error_code: _Optional[_Union[_move_it_error_codes_pb2.MoveItErrorCodes, _Mapping]] = ...) -> None: ...
