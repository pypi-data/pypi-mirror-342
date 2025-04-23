from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.humble.rc_common_msgs.msg import return_code_pb2 as _return_code_pb2
from make87_messages_ros2.humble.shape_msgs.msg import plane_pb2 as _plane_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetBasePlaneCalibrationRequest(_message.Message):
    __slots__ = ["header", "pose_frame", "robot_pose"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    POSE_FRAME_FIELD_NUMBER: _ClassVar[int]
    ROBOT_POSE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    pose_frame: str
    robot_pose: _pose_pb2.Pose
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., pose_frame: _Optional[str] = ..., robot_pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ...) -> None: ...

class GetBasePlaneCalibrationResponse(_message.Message):
    __slots__ = ["header", "pose_frame", "plane", "return_code"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    POSE_FRAME_FIELD_NUMBER: _ClassVar[int]
    PLANE_FIELD_NUMBER: _ClassVar[int]
    RETURN_CODE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    pose_frame: str
    plane: _plane_pb2.Plane
    return_code: _return_code_pb2.ReturnCode
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., pose_frame: _Optional[str] = ..., plane: _Optional[_Union[_plane_pb2.Plane, _Mapping]] = ..., return_code: _Optional[_Union[_return_code_pb2.ReturnCode, _Mapping]] = ...) -> None: ...
