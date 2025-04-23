from make87_messages_ros2.jazzy.sensor_msgs.msg import imu_pb2 as _imu_pb2
from make87_messages_ros2.jazzy.sensor_msgs.msg import magnetic_field_pb2 as _magnetic_field_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ImuWithMagneticField(_message.Message):
    __slots__ = ["header", "imu", "field"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    IMU_FIELD_NUMBER: _ClassVar[int]
    FIELD_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    imu: _imu_pb2.Imu
    field: _magnetic_field_pb2.MagneticField
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., imu: _Optional[_Union[_imu_pb2.Imu, _Mapping]] = ..., field: _Optional[_Union[_magnetic_field_pb2.MagneticField, _Mapping]] = ...) -> None: ...
