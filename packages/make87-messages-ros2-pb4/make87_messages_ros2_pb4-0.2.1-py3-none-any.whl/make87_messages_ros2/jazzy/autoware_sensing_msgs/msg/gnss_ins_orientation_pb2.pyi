from make87_messages_ros2.jazzy.geometry_msgs.msg import quaternion_pb2 as _quaternion_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GnssInsOrientation(_message.Message):
    __slots__ = ["orientation", "rmse_rotation_x", "rmse_rotation_y", "rmse_rotation_z"]
    ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    RMSE_ROTATION_X_FIELD_NUMBER: _ClassVar[int]
    RMSE_ROTATION_Y_FIELD_NUMBER: _ClassVar[int]
    RMSE_ROTATION_Z_FIELD_NUMBER: _ClassVar[int]
    orientation: _quaternion_pb2.Quaternion
    rmse_rotation_x: float
    rmse_rotation_y: float
    rmse_rotation_z: float
    def __init__(self, orientation: _Optional[_Union[_quaternion_pb2.Quaternion, _Mapping]] = ..., rmse_rotation_x: _Optional[float] = ..., rmse_rotation_y: _Optional[float] = ..., rmse_rotation_z: _Optional[float] = ...) -> None: ...
