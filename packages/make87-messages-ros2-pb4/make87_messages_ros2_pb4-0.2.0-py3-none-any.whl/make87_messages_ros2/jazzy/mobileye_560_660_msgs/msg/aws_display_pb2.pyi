from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AwsDisplay(_message.Message):
    __slots__ = ["header", "suppress_sound", "night_time", "dusk_time", "sound_type", "headway_valid", "headway_measurement", "lanes_on", "left_ldw_on", "right_ldw_on", "fcw_on", "left_crossing", "right_crossing", "maintenance", "failsafe", "ped_fcw", "ped_in_dz", "headway_warning_level"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUPPRESS_SOUND_FIELD_NUMBER: _ClassVar[int]
    NIGHT_TIME_FIELD_NUMBER: _ClassVar[int]
    DUSK_TIME_FIELD_NUMBER: _ClassVar[int]
    SOUND_TYPE_FIELD_NUMBER: _ClassVar[int]
    HEADWAY_VALID_FIELD_NUMBER: _ClassVar[int]
    HEADWAY_MEASUREMENT_FIELD_NUMBER: _ClassVar[int]
    LANES_ON_FIELD_NUMBER: _ClassVar[int]
    LEFT_LDW_ON_FIELD_NUMBER: _ClassVar[int]
    RIGHT_LDW_ON_FIELD_NUMBER: _ClassVar[int]
    FCW_ON_FIELD_NUMBER: _ClassVar[int]
    LEFT_CROSSING_FIELD_NUMBER: _ClassVar[int]
    RIGHT_CROSSING_FIELD_NUMBER: _ClassVar[int]
    MAINTENANCE_FIELD_NUMBER: _ClassVar[int]
    FAILSAFE_FIELD_NUMBER: _ClassVar[int]
    PED_FCW_FIELD_NUMBER: _ClassVar[int]
    PED_IN_DZ_FIELD_NUMBER: _ClassVar[int]
    HEADWAY_WARNING_LEVEL_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    suppress_sound: bool
    night_time: bool
    dusk_time: bool
    sound_type: int
    headway_valid: bool
    headway_measurement: float
    lanes_on: bool
    left_ldw_on: bool
    right_ldw_on: bool
    fcw_on: bool
    left_crossing: bool
    right_crossing: bool
    maintenance: bool
    failsafe: bool
    ped_fcw: bool
    ped_in_dz: bool
    headway_warning_level: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., suppress_sound: bool = ..., night_time: bool = ..., dusk_time: bool = ..., sound_type: _Optional[int] = ..., headway_valid: bool = ..., headway_measurement: _Optional[float] = ..., lanes_on: bool = ..., left_ldw_on: bool = ..., right_ldw_on: bool = ..., fcw_on: bool = ..., left_crossing: bool = ..., right_crossing: bool = ..., maintenance: bool = ..., failsafe: bool = ..., ped_fcw: bool = ..., ped_in_dz: bool = ..., headway_warning_level: _Optional[int] = ...) -> None: ...
