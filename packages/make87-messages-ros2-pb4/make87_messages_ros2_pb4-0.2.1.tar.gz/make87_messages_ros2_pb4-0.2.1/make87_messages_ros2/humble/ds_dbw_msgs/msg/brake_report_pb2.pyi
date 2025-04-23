from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.ds_dbw_msgs.msg import cmd_src_pb2 as _cmd_src_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BrakeReport(_message.Message):
    __slots__ = ["header", "ros2_header", "cmd_type", "pressure_input", "pressure_cmd", "pressure_output", "torque_input", "torque_cmd", "torque_output", "accel_cmd", "accel_output", "percent_input", "percent_cmd", "percent_output", "btsi_cmd", "yield_request", "limiting_value", "limiting_rate", "external_control", "ready", "enabled", "override_active", "override_other", "override_latched", "timeout", "fault", "bad_crc", "bad_rc", "degraded", "limit_value", "brake_available_duration", "brake_available_full", "req_shift_park", "req_park_brake", "external_button", "comms_loss_armed", "cmd_src"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    CMD_TYPE_FIELD_NUMBER: _ClassVar[int]
    PRESSURE_INPUT_FIELD_NUMBER: _ClassVar[int]
    PRESSURE_CMD_FIELD_NUMBER: _ClassVar[int]
    PRESSURE_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    TORQUE_INPUT_FIELD_NUMBER: _ClassVar[int]
    TORQUE_CMD_FIELD_NUMBER: _ClassVar[int]
    TORQUE_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    ACCEL_CMD_FIELD_NUMBER: _ClassVar[int]
    ACCEL_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    PERCENT_INPUT_FIELD_NUMBER: _ClassVar[int]
    PERCENT_CMD_FIELD_NUMBER: _ClassVar[int]
    PERCENT_OUTPUT_FIELD_NUMBER: _ClassVar[int]
    BTSI_CMD_FIELD_NUMBER: _ClassVar[int]
    YIELD_REQUEST_FIELD_NUMBER: _ClassVar[int]
    LIMITING_VALUE_FIELD_NUMBER: _ClassVar[int]
    LIMITING_RATE_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_CONTROL_FIELD_NUMBER: _ClassVar[int]
    READY_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_OTHER_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_LATCHED_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    FAULT_FIELD_NUMBER: _ClassVar[int]
    BAD_CRC_FIELD_NUMBER: _ClassVar[int]
    BAD_RC_FIELD_NUMBER: _ClassVar[int]
    DEGRADED_FIELD_NUMBER: _ClassVar[int]
    LIMIT_VALUE_FIELD_NUMBER: _ClassVar[int]
    BRAKE_AVAILABLE_DURATION_FIELD_NUMBER: _ClassVar[int]
    BRAKE_AVAILABLE_FULL_FIELD_NUMBER: _ClassVar[int]
    REQ_SHIFT_PARK_FIELD_NUMBER: _ClassVar[int]
    REQ_PARK_BRAKE_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_BUTTON_FIELD_NUMBER: _ClassVar[int]
    COMMS_LOSS_ARMED_FIELD_NUMBER: _ClassVar[int]
    CMD_SRC_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    cmd_type: int
    pressure_input: float
    pressure_cmd: float
    pressure_output: float
    torque_input: float
    torque_cmd: float
    torque_output: float
    accel_cmd: float
    accel_output: float
    percent_input: float
    percent_cmd: float
    percent_output: float
    btsi_cmd: bool
    yield_request: bool
    limiting_value: bool
    limiting_rate: bool
    external_control: bool
    ready: bool
    enabled: bool
    override_active: bool
    override_other: bool
    override_latched: bool
    timeout: bool
    fault: bool
    bad_crc: bool
    bad_rc: bool
    degraded: bool
    limit_value: float
    brake_available_duration: float
    brake_available_full: bool
    req_shift_park: bool
    req_park_brake: bool
    external_button: bool
    comms_loss_armed: bool
    cmd_src: _cmd_src_pb2.CmdSrc
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., cmd_type: _Optional[int] = ..., pressure_input: _Optional[float] = ..., pressure_cmd: _Optional[float] = ..., pressure_output: _Optional[float] = ..., torque_input: _Optional[float] = ..., torque_cmd: _Optional[float] = ..., torque_output: _Optional[float] = ..., accel_cmd: _Optional[float] = ..., accel_output: _Optional[float] = ..., percent_input: _Optional[float] = ..., percent_cmd: _Optional[float] = ..., percent_output: _Optional[float] = ..., btsi_cmd: bool = ..., yield_request: bool = ..., limiting_value: bool = ..., limiting_rate: bool = ..., external_control: bool = ..., ready: bool = ..., enabled: bool = ..., override_active: bool = ..., override_other: bool = ..., override_latched: bool = ..., timeout: bool = ..., fault: bool = ..., bad_crc: bool = ..., bad_rc: bool = ..., degraded: bool = ..., limit_value: _Optional[float] = ..., brake_available_duration: _Optional[float] = ..., brake_available_full: bool = ..., req_shift_park: bool = ..., req_park_brake: bool = ..., external_button: bool = ..., comms_loss_armed: bool = ..., cmd_src: _Optional[_Union[_cmd_src_pb2.CmdSrc, _Mapping]] = ...) -> None: ...
