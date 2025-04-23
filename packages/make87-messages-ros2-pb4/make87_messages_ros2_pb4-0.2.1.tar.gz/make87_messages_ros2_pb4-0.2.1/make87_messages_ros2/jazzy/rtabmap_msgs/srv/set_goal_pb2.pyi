from make87_messages_ros2.jazzy.geometry_msgs.msg import pose_pb2 as _pose_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetGoalRequest(_message.Message):
    __slots__ = ["node_id", "node_label", "frame_id"]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    NODE_LABEL_FIELD_NUMBER: _ClassVar[int]
    FRAME_ID_FIELD_NUMBER: _ClassVar[int]
    node_id: int
    node_label: str
    frame_id: str
    def __init__(self, node_id: _Optional[int] = ..., node_label: _Optional[str] = ..., frame_id: _Optional[str] = ...) -> None: ...

class SetGoalResponse(_message.Message):
    __slots__ = ["path_ids", "path_poses", "planning_time"]
    PATH_IDS_FIELD_NUMBER: _ClassVar[int]
    PATH_POSES_FIELD_NUMBER: _ClassVar[int]
    PLANNING_TIME_FIELD_NUMBER: _ClassVar[int]
    path_ids: _containers.RepeatedScalarFieldContainer[int]
    path_poses: _containers.RepeatedCompositeFieldContainer[_pose_pb2.Pose]
    planning_time: float
    def __init__(self, path_ids: _Optional[_Iterable[int]] = ..., path_poses: _Optional[_Iterable[_Union[_pose_pb2.Pose, _Mapping]]] = ..., planning_time: _Optional[float] = ...) -> None: ...
