from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.cartographer_ros_msgs.msg import status_response_pb2 as _status_response_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_pb2 as _pose_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StartTrajectoryRequest(_message.Message):
    __slots__ = ["header", "configuration_directory", "configuration_basename", "use_initial_pose", "initial_pose", "relative_to_trajectory_id"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CONFIGURATION_DIRECTORY_FIELD_NUMBER: _ClassVar[int]
    CONFIGURATION_BASENAME_FIELD_NUMBER: _ClassVar[int]
    USE_INITIAL_POSE_FIELD_NUMBER: _ClassVar[int]
    INITIAL_POSE_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_TO_TRAJECTORY_ID_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    configuration_directory: str
    configuration_basename: str
    use_initial_pose: bool
    initial_pose: _pose_pb2.Pose
    relative_to_trajectory_id: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., configuration_directory: _Optional[str] = ..., configuration_basename: _Optional[str] = ..., use_initial_pose: bool = ..., initial_pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., relative_to_trajectory_id: _Optional[int] = ...) -> None: ...

class StartTrajectoryResponse(_message.Message):
    __slots__ = ["header", "status", "trajectory_id"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TRAJECTORY_ID_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    status: _status_response_pb2.StatusResponse
    trajectory_id: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., status: _Optional[_Union[_status_response_pb2.StatusResponse, _Mapping]] = ..., trajectory_id: _Optional[int] = ...) -> None: ...
