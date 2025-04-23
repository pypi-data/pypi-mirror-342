from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_pb2 as _pose_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetLinkPropertiesRequest(_message.Message):
    __slots__ = ["header", "link_name", "com", "gravity_mode", "mass", "ixx", "ixy", "ixz", "iyy", "iyz", "izz"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    LINK_NAME_FIELD_NUMBER: _ClassVar[int]
    COM_FIELD_NUMBER: _ClassVar[int]
    GRAVITY_MODE_FIELD_NUMBER: _ClassVar[int]
    MASS_FIELD_NUMBER: _ClassVar[int]
    IXX_FIELD_NUMBER: _ClassVar[int]
    IXY_FIELD_NUMBER: _ClassVar[int]
    IXZ_FIELD_NUMBER: _ClassVar[int]
    IYY_FIELD_NUMBER: _ClassVar[int]
    IYZ_FIELD_NUMBER: _ClassVar[int]
    IZZ_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    link_name: str
    com: _pose_pb2.Pose
    gravity_mode: bool
    mass: float
    ixx: float
    ixy: float
    ixz: float
    iyy: float
    iyz: float
    izz: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., link_name: _Optional[str] = ..., com: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., gravity_mode: bool = ..., mass: _Optional[float] = ..., ixx: _Optional[float] = ..., ixy: _Optional[float] = ..., ixz: _Optional[float] = ..., iyy: _Optional[float] = ..., iyz: _Optional[float] = ..., izz: _Optional[float] = ...) -> None: ...

class SetLinkPropertiesResponse(_message.Message):
    __slots__ = ["header", "success", "status_message"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    status_message: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., status_message: _Optional[str] = ...) -> None: ...
