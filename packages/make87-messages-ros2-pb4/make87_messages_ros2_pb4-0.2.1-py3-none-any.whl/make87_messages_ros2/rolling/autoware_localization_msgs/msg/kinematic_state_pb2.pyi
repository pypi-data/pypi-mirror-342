from make87_messages_ros2.rolling.geometry_msgs.msg import accel_with_covariance_pb2 as _accel_with_covariance_pb2
from make87_messages_ros2.rolling.geometry_msgs.msg import pose_with_covariance_pb2 as _pose_with_covariance_pb2
from make87_messages_ros2.rolling.geometry_msgs.msg import twist_with_covariance_pb2 as _twist_with_covariance_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class KinematicState(_message.Message):
    __slots__ = ["header", "child_frame_id", "pose_with_covariance", "twist_with_covariance", "accel_with_covariance"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CHILD_FRAME_ID_FIELD_NUMBER: _ClassVar[int]
    POSE_WITH_COVARIANCE_FIELD_NUMBER: _ClassVar[int]
    TWIST_WITH_COVARIANCE_FIELD_NUMBER: _ClassVar[int]
    ACCEL_WITH_COVARIANCE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    child_frame_id: str
    pose_with_covariance: _pose_with_covariance_pb2.PoseWithCovariance
    twist_with_covariance: _twist_with_covariance_pb2.TwistWithCovariance
    accel_with_covariance: _accel_with_covariance_pb2.AccelWithCovariance
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., child_frame_id: _Optional[str] = ..., pose_with_covariance: _Optional[_Union[_pose_with_covariance_pb2.PoseWithCovariance, _Mapping]] = ..., twist_with_covariance: _Optional[_Union[_twist_with_covariance_pb2.TwistWithCovariance, _Mapping]] = ..., accel_with_covariance: _Optional[_Union[_accel_with_covariance_pb2.AccelWithCovariance, _Mapping]] = ...) -> None: ...
