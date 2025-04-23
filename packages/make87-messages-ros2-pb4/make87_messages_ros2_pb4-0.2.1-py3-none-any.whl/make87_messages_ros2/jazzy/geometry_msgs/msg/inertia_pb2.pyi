from make87_messages_ros2.jazzy.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Inertia(_message.Message):
    __slots__ = ["m", "com", "ixx", "ixy", "ixz", "iyy", "iyz", "izz"]
    M_FIELD_NUMBER: _ClassVar[int]
    COM_FIELD_NUMBER: _ClassVar[int]
    IXX_FIELD_NUMBER: _ClassVar[int]
    IXY_FIELD_NUMBER: _ClassVar[int]
    IXZ_FIELD_NUMBER: _ClassVar[int]
    IYY_FIELD_NUMBER: _ClassVar[int]
    IYZ_FIELD_NUMBER: _ClassVar[int]
    IZZ_FIELD_NUMBER: _ClassVar[int]
    m: float
    com: _vector3_pb2.Vector3
    ixx: float
    ixy: float
    ixz: float
    iyy: float
    iyz: float
    izz: float
    def __init__(self, m: _Optional[float] = ..., com: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., ixx: _Optional[float] = ..., ixy: _Optional[float] = ..., ixz: _Optional[float] = ..., iyy: _Optional[float] = ..., iyz: _Optional[float] = ..., izz: _Optional[float] = ...) -> None: ...
