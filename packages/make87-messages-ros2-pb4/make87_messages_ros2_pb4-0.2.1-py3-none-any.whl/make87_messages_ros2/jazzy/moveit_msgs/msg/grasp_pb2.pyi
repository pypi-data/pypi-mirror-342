from make87_messages_ros2.jazzy.geometry_msgs.msg import pose_stamped_pb2 as _pose_stamped_pb2
from make87_messages_ros2.jazzy.moveit_msgs.msg import gripper_translation_pb2 as _gripper_translation_pb2
from make87_messages_ros2.jazzy.trajectory_msgs.msg import joint_trajectory_pb2 as _joint_trajectory_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Grasp(_message.Message):
    __slots__ = ["id", "pre_grasp_posture", "grasp_posture", "grasp_pose", "grasp_quality", "pre_grasp_approach", "post_grasp_retreat", "post_place_retreat", "max_contact_force", "allowed_touch_objects"]
    ID_FIELD_NUMBER: _ClassVar[int]
    PRE_GRASP_POSTURE_FIELD_NUMBER: _ClassVar[int]
    GRASP_POSTURE_FIELD_NUMBER: _ClassVar[int]
    GRASP_POSE_FIELD_NUMBER: _ClassVar[int]
    GRASP_QUALITY_FIELD_NUMBER: _ClassVar[int]
    PRE_GRASP_APPROACH_FIELD_NUMBER: _ClassVar[int]
    POST_GRASP_RETREAT_FIELD_NUMBER: _ClassVar[int]
    POST_PLACE_RETREAT_FIELD_NUMBER: _ClassVar[int]
    MAX_CONTACT_FORCE_FIELD_NUMBER: _ClassVar[int]
    ALLOWED_TOUCH_OBJECTS_FIELD_NUMBER: _ClassVar[int]
    id: str
    pre_grasp_posture: _joint_trajectory_pb2.JointTrajectory
    grasp_posture: _joint_trajectory_pb2.JointTrajectory
    grasp_pose: _pose_stamped_pb2.PoseStamped
    grasp_quality: float
    pre_grasp_approach: _gripper_translation_pb2.GripperTranslation
    post_grasp_retreat: _gripper_translation_pb2.GripperTranslation
    post_place_retreat: _gripper_translation_pb2.GripperTranslation
    max_contact_force: float
    allowed_touch_objects: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[str] = ..., pre_grasp_posture: _Optional[_Union[_joint_trajectory_pb2.JointTrajectory, _Mapping]] = ..., grasp_posture: _Optional[_Union[_joint_trajectory_pb2.JointTrajectory, _Mapping]] = ..., grasp_pose: _Optional[_Union[_pose_stamped_pb2.PoseStamped, _Mapping]] = ..., grasp_quality: _Optional[float] = ..., pre_grasp_approach: _Optional[_Union[_gripper_translation_pb2.GripperTranslation, _Mapping]] = ..., post_grasp_retreat: _Optional[_Union[_gripper_translation_pb2.GripperTranslation, _Mapping]] = ..., post_place_retreat: _Optional[_Union[_gripper_translation_pb2.GripperTranslation, _Mapping]] = ..., max_contact_force: _Optional[float] = ..., allowed_touch_objects: _Optional[_Iterable[str]] = ...) -> None: ...
