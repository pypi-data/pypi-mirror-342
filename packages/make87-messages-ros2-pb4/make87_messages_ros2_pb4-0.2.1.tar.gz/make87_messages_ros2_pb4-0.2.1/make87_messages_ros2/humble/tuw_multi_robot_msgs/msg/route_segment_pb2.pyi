from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.humble.tuw_multi_robot_msgs.msg import route_precondition_pb2 as _route_precondition_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RouteSegment(_message.Message):
    __slots__ = ["header", "segment_id", "preconditions", "start", "end", "width"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SEGMENT_ID_FIELD_NUMBER: _ClassVar[int]
    PRECONDITIONS_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    segment_id: int
    preconditions: _containers.RepeatedCompositeFieldContainer[_route_precondition_pb2.RoutePrecondition]
    start: _pose_pb2.Pose
    end: _pose_pb2.Pose
    width: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., segment_id: _Optional[int] = ..., preconditions: _Optional[_Iterable[_Union[_route_precondition_pb2.RoutePrecondition, _Mapping]]] = ..., start: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., end: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., width: _Optional[float] = ...) -> None: ...
