from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.ds_dbw_msgs.msg import drive_mode_pb2 as _drive_mode_pb2
from make87_messages_ros2.humble.ds_dbw_msgs.msg import gear_num_pb2 as _gear_num_pb2
from make87_messages_ros2.humble.ds_dbw_msgs.msg import one_pedal_pb2 as _one_pedal_pb2
from make87_messages_ros2.humble.ds_dbw_msgs.msg import quality_pb2 as _quality_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ThrottleInfo(_message.Message):
    __slots__ = ["header", "ros2_header", "accel_pedal_pc", "accel_pedal_qf", "one_pedal", "engine_rpm", "drive_mode", "gear_num"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    ACCEL_PEDAL_PC_FIELD_NUMBER: _ClassVar[int]
    ACCEL_PEDAL_QF_FIELD_NUMBER: _ClassVar[int]
    ONE_PEDAL_FIELD_NUMBER: _ClassVar[int]
    ENGINE_RPM_FIELD_NUMBER: _ClassVar[int]
    DRIVE_MODE_FIELD_NUMBER: _ClassVar[int]
    GEAR_NUM_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    accel_pedal_pc: float
    accel_pedal_qf: _quality_pb2.Quality
    one_pedal: _one_pedal_pb2.OnePedal
    engine_rpm: float
    drive_mode: _drive_mode_pb2.DriveMode
    gear_num: _gear_num_pb2.GearNum
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., accel_pedal_pc: _Optional[float] = ..., accel_pedal_qf: _Optional[_Union[_quality_pb2.Quality, _Mapping]] = ..., one_pedal: _Optional[_Union[_one_pedal_pb2.OnePedal, _Mapping]] = ..., engine_rpm: _Optional[float] = ..., drive_mode: _Optional[_Union[_drive_mode_pb2.DriveMode, _Mapping]] = ..., gear_num: _Optional[_Union[_gear_num_pb2.GearNum, _Mapping]] = ...) -> None: ...
