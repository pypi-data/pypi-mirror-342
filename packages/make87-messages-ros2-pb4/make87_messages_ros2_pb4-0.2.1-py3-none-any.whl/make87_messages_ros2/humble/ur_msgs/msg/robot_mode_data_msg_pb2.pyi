from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RobotModeDataMsg(_message.Message):
    __slots__ = ["header", "timestamp", "is_robot_connected", "is_real_robot_enabled", "is_power_on_robot", "is_emergency_stopped", "is_protective_stopped", "is_program_running", "is_program_paused"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    IS_ROBOT_CONNECTED_FIELD_NUMBER: _ClassVar[int]
    IS_REAL_ROBOT_ENABLED_FIELD_NUMBER: _ClassVar[int]
    IS_POWER_ON_ROBOT_FIELD_NUMBER: _ClassVar[int]
    IS_EMERGENCY_STOPPED_FIELD_NUMBER: _ClassVar[int]
    IS_PROTECTIVE_STOPPED_FIELD_NUMBER: _ClassVar[int]
    IS_PROGRAM_RUNNING_FIELD_NUMBER: _ClassVar[int]
    IS_PROGRAM_PAUSED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    timestamp: int
    is_robot_connected: bool
    is_real_robot_enabled: bool
    is_power_on_robot: bool
    is_emergency_stopped: bool
    is_protective_stopped: bool
    is_program_running: bool
    is_program_paused: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., timestamp: _Optional[int] = ..., is_robot_connected: bool = ..., is_real_robot_enabled: bool = ..., is_power_on_robot: bool = ..., is_emergency_stopped: bool = ..., is_protective_stopped: bool = ..., is_program_running: bool = ..., is_program_paused: bool = ...) -> None: ...
