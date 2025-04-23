from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_stamped_pb2 as _pose_stamped_pb2
from make87_messages_ros2.humble.rtabmap_msgs.msg import path_pb2 as _path_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetPlanRequest(_message.Message):
    __slots__ = ["header", "goal_node", "goal", "tolerance"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    GOAL_NODE_FIELD_NUMBER: _ClassVar[int]
    GOAL_FIELD_NUMBER: _ClassVar[int]
    TOLERANCE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    goal_node: int
    goal: _pose_stamped_pb2.PoseStamped
    tolerance: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., goal_node: _Optional[int] = ..., goal: _Optional[_Union[_pose_stamped_pb2.PoseStamped, _Mapping]] = ..., tolerance: _Optional[float] = ...) -> None: ...

class GetPlanResponse(_message.Message):
    __slots__ = ["header", "plan"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PLAN_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    plan: _path_pb2.Path
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., plan: _Optional[_Union[_path_pb2.Path, _Mapping]] = ...) -> None: ...
