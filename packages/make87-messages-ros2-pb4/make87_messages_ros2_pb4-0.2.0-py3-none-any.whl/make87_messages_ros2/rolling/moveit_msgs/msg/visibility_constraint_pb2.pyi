from make87_messages_ros2.rolling.geometry_msgs.msg import pose_stamped_pb2 as _pose_stamped_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VisibilityConstraint(_message.Message):
    __slots__ = ["target_radius", "target_pose", "cone_sides", "sensor_pose", "max_view_angle", "max_range_angle", "sensor_view_direction", "weight"]
    TARGET_RADIUS_FIELD_NUMBER: _ClassVar[int]
    TARGET_POSE_FIELD_NUMBER: _ClassVar[int]
    CONE_SIDES_FIELD_NUMBER: _ClassVar[int]
    SENSOR_POSE_FIELD_NUMBER: _ClassVar[int]
    MAX_VIEW_ANGLE_FIELD_NUMBER: _ClassVar[int]
    MAX_RANGE_ANGLE_FIELD_NUMBER: _ClassVar[int]
    SENSOR_VIEW_DIRECTION_FIELD_NUMBER: _ClassVar[int]
    WEIGHT_FIELD_NUMBER: _ClassVar[int]
    target_radius: float
    target_pose: _pose_stamped_pb2.PoseStamped
    cone_sides: int
    sensor_pose: _pose_stamped_pb2.PoseStamped
    max_view_angle: float
    max_range_angle: float
    sensor_view_direction: int
    weight: float
    def __init__(self, target_radius: _Optional[float] = ..., target_pose: _Optional[_Union[_pose_stamped_pb2.PoseStamped, _Mapping]] = ..., cone_sides: _Optional[int] = ..., sensor_pose: _Optional[_Union[_pose_stamped_pb2.PoseStamped, _Mapping]] = ..., max_view_angle: _Optional[float] = ..., max_range_angle: _Optional[float] = ..., sensor_view_direction: _Optional[int] = ..., weight: _Optional[float] = ...) -> None: ...
