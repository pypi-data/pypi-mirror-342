from make87_messages_ros2.jazzy.novatel_gps_msgs.msg import novatel_extended_solution_status_pb2 as _novatel_extended_solution_status_pb2
from make87_messages_ros2.jazzy.novatel_gps_msgs.msg import novatel_message_header_pb2 as _novatel_message_header_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Inspvax(_message.Message):
    __slots__ = ["header", "novatel_msg_header", "ins_status", "position_type", "latitude", "longitude", "altitude", "undulation", "north_velocity", "east_velocity", "up_velocity", "roll", "pitch", "azimuth", "latitude_std", "longitude_std", "altitude_std", "north_velocity_std", "east_velocity_std", "up_velocity_std", "roll_std", "pitch_std", "azimuth_std", "extended_status", "seconds_since_update"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NOVATEL_MSG_HEADER_FIELD_NUMBER: _ClassVar[int]
    INS_STATUS_FIELD_NUMBER: _ClassVar[int]
    POSITION_TYPE_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_FIELD_NUMBER: _ClassVar[int]
    UNDULATION_FIELD_NUMBER: _ClassVar[int]
    NORTH_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    EAST_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    UP_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    ROLL_FIELD_NUMBER: _ClassVar[int]
    PITCH_FIELD_NUMBER: _ClassVar[int]
    AZIMUTH_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_STD_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_STD_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_STD_FIELD_NUMBER: _ClassVar[int]
    NORTH_VELOCITY_STD_FIELD_NUMBER: _ClassVar[int]
    EAST_VELOCITY_STD_FIELD_NUMBER: _ClassVar[int]
    UP_VELOCITY_STD_FIELD_NUMBER: _ClassVar[int]
    ROLL_STD_FIELD_NUMBER: _ClassVar[int]
    PITCH_STD_FIELD_NUMBER: _ClassVar[int]
    AZIMUTH_STD_FIELD_NUMBER: _ClassVar[int]
    EXTENDED_STATUS_FIELD_NUMBER: _ClassVar[int]
    SECONDS_SINCE_UPDATE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    novatel_msg_header: _novatel_message_header_pb2.NovatelMessageHeader
    ins_status: str
    position_type: str
    latitude: float
    longitude: float
    altitude: float
    undulation: float
    north_velocity: float
    east_velocity: float
    up_velocity: float
    roll: float
    pitch: float
    azimuth: float
    latitude_std: float
    longitude_std: float
    altitude_std: float
    north_velocity_std: float
    east_velocity_std: float
    up_velocity_std: float
    roll_std: float
    pitch_std: float
    azimuth_std: float
    extended_status: _novatel_extended_solution_status_pb2.NovatelExtendedSolutionStatus
    seconds_since_update: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., novatel_msg_header: _Optional[_Union[_novatel_message_header_pb2.NovatelMessageHeader, _Mapping]] = ..., ins_status: _Optional[str] = ..., position_type: _Optional[str] = ..., latitude: _Optional[float] = ..., longitude: _Optional[float] = ..., altitude: _Optional[float] = ..., undulation: _Optional[float] = ..., north_velocity: _Optional[float] = ..., east_velocity: _Optional[float] = ..., up_velocity: _Optional[float] = ..., roll: _Optional[float] = ..., pitch: _Optional[float] = ..., azimuth: _Optional[float] = ..., latitude_std: _Optional[float] = ..., longitude_std: _Optional[float] = ..., altitude_std: _Optional[float] = ..., north_velocity_std: _Optional[float] = ..., east_velocity_std: _Optional[float] = ..., up_velocity_std: _Optional[float] = ..., roll_std: _Optional[float] = ..., pitch_std: _Optional[float] = ..., azimuth_std: _Optional[float] = ..., extended_status: _Optional[_Union[_novatel_extended_solution_status_pb2.NovatelExtendedSolutionStatus, _Mapping]] = ..., seconds_since_update: _Optional[int] = ...) -> None: ...
