from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_with_covariance_pb2 as _pose_with_covariance_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from make87_messages_ros2.humble.tuw_multi_robot_msgs.msg import route_precondition_pb2 as _route_precondition_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RobotInfo(_message.Message):
    __slots__ = ["header", "ros2_header", "robot_name", "pose", "shape", "shape_variables", "sync", "mode", "status", "good_id", "order_id", "order_status"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    ROBOT_NAME_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    SHAPE_FIELD_NUMBER: _ClassVar[int]
    SHAPE_VARIABLES_FIELD_NUMBER: _ClassVar[int]
    SYNC_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    GOOD_ID_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    ORDER_STATUS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    robot_name: str
    pose: _pose_with_covariance_pb2.PoseWithCovariance
    shape: int
    shape_variables: _containers.RepeatedScalarFieldContainer[float]
    sync: _route_precondition_pb2.RoutePrecondition
    mode: int
    status: int
    good_id: int
    order_id: int
    order_status: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., robot_name: _Optional[str] = ..., pose: _Optional[_Union[_pose_with_covariance_pb2.PoseWithCovariance, _Mapping]] = ..., shape: _Optional[int] = ..., shape_variables: _Optional[_Iterable[float]] = ..., sync: _Optional[_Union[_route_precondition_pb2.RoutePrecondition, _Mapping]] = ..., mode: _Optional[int] = ..., status: _Optional[int] = ..., good_id: _Optional[int] = ..., order_id: _Optional[int] = ..., order_status: _Optional[int] = ...) -> None: ...
