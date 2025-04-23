from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UlcReport(_message.Message):
    __slots__ = ["header", "ros2_header", "cmd_type", "vel_ref", "vel_meas", "accel_ref", "accel_meas", "coast_decel", "ready", "enabled", "override_active", "override_latched", "preempted", "timeout", "bad_crc", "bad_rc"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    CMD_TYPE_FIELD_NUMBER: _ClassVar[int]
    VEL_REF_FIELD_NUMBER: _ClassVar[int]
    VEL_MEAS_FIELD_NUMBER: _ClassVar[int]
    ACCEL_REF_FIELD_NUMBER: _ClassVar[int]
    ACCEL_MEAS_FIELD_NUMBER: _ClassVar[int]
    COAST_DECEL_FIELD_NUMBER: _ClassVar[int]
    READY_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_LATCHED_FIELD_NUMBER: _ClassVar[int]
    PREEMPTED_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    BAD_CRC_FIELD_NUMBER: _ClassVar[int]
    BAD_RC_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    cmd_type: int
    vel_ref: float
    vel_meas: float
    accel_ref: float
    accel_meas: float
    coast_decel: bool
    ready: bool
    enabled: bool
    override_active: bool
    override_latched: bool
    preempted: bool
    timeout: bool
    bad_crc: bool
    bad_rc: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., cmd_type: _Optional[int] = ..., vel_ref: _Optional[float] = ..., vel_meas: _Optional[float] = ..., accel_ref: _Optional[float] = ..., accel_meas: _Optional[float] = ..., coast_decel: bool = ..., ready: bool = ..., enabled: bool = ..., override_active: bool = ..., override_latched: bool = ..., preempted: bool = ..., timeout: bool = ..., bad_crc: bool = ..., bad_rc: bool = ...) -> None: ...
