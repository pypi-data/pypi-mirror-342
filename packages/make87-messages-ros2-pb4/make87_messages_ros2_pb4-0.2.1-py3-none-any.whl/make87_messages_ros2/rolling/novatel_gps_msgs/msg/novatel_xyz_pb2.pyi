from make87_messages_ros2.rolling.novatel_gps_msgs.msg import novatel_extended_solution_status_pb2 as _novatel_extended_solution_status_pb2
from make87_messages_ros2.rolling.novatel_gps_msgs.msg import novatel_message_header_pb2 as _novatel_message_header_pb2
from make87_messages_ros2.rolling.novatel_gps_msgs.msg import novatel_signal_mask_pb2 as _novatel_signal_mask_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NovatelXYZ(_message.Message):
    __slots__ = ["header", "novatel_msg_header", "solution_status", "position_type", "x", "y", "z", "x_sigma", "y_sigma", "z_sigma", "velocity_solution_status", "velocity_type", "x_vel", "y_vel", "z_vel", "x_vel_sigma", "y_vel_sigma", "z_vel_sigma", "base_station_id", "velocity_latency", "diff_age", "solution_age", "num_satellites_tracked", "num_satellites_used_in_solution", "num_gps_and_glonass_l1_used_in_solution", "num_gps_and_glonass_l1_and_l2_used_in_solution", "extended_solution_status", "signal_mask"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NOVATEL_MSG_HEADER_FIELD_NUMBER: _ClassVar[int]
    SOLUTION_STATUS_FIELD_NUMBER: _ClassVar[int]
    POSITION_TYPE_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    X_SIGMA_FIELD_NUMBER: _ClassVar[int]
    Y_SIGMA_FIELD_NUMBER: _ClassVar[int]
    Z_SIGMA_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_SOLUTION_STATUS_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_TYPE_FIELD_NUMBER: _ClassVar[int]
    X_VEL_FIELD_NUMBER: _ClassVar[int]
    Y_VEL_FIELD_NUMBER: _ClassVar[int]
    Z_VEL_FIELD_NUMBER: _ClassVar[int]
    X_VEL_SIGMA_FIELD_NUMBER: _ClassVar[int]
    Y_VEL_SIGMA_FIELD_NUMBER: _ClassVar[int]
    Z_VEL_SIGMA_FIELD_NUMBER: _ClassVar[int]
    BASE_STATION_ID_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_LATENCY_FIELD_NUMBER: _ClassVar[int]
    DIFF_AGE_FIELD_NUMBER: _ClassVar[int]
    SOLUTION_AGE_FIELD_NUMBER: _ClassVar[int]
    NUM_SATELLITES_TRACKED_FIELD_NUMBER: _ClassVar[int]
    NUM_SATELLITES_USED_IN_SOLUTION_FIELD_NUMBER: _ClassVar[int]
    NUM_GPS_AND_GLONASS_L1_USED_IN_SOLUTION_FIELD_NUMBER: _ClassVar[int]
    NUM_GPS_AND_GLONASS_L1_AND_L2_USED_IN_SOLUTION_FIELD_NUMBER: _ClassVar[int]
    EXTENDED_SOLUTION_STATUS_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_MASK_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    novatel_msg_header: _novatel_message_header_pb2.NovatelMessageHeader
    solution_status: str
    position_type: str
    x: float
    y: float
    z: float
    x_sigma: float
    y_sigma: float
    z_sigma: float
    velocity_solution_status: str
    velocity_type: str
    x_vel: float
    y_vel: float
    z_vel: float
    x_vel_sigma: float
    y_vel_sigma: float
    z_vel_sigma: float
    base_station_id: str
    velocity_latency: float
    diff_age: float
    solution_age: float
    num_satellites_tracked: int
    num_satellites_used_in_solution: int
    num_gps_and_glonass_l1_used_in_solution: int
    num_gps_and_glonass_l1_and_l2_used_in_solution: int
    extended_solution_status: _novatel_extended_solution_status_pb2.NovatelExtendedSolutionStatus
    signal_mask: _novatel_signal_mask_pb2.NovatelSignalMask
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., novatel_msg_header: _Optional[_Union[_novatel_message_header_pb2.NovatelMessageHeader, _Mapping]] = ..., solution_status: _Optional[str] = ..., position_type: _Optional[str] = ..., x: _Optional[float] = ..., y: _Optional[float] = ..., z: _Optional[float] = ..., x_sigma: _Optional[float] = ..., y_sigma: _Optional[float] = ..., z_sigma: _Optional[float] = ..., velocity_solution_status: _Optional[str] = ..., velocity_type: _Optional[str] = ..., x_vel: _Optional[float] = ..., y_vel: _Optional[float] = ..., z_vel: _Optional[float] = ..., x_vel_sigma: _Optional[float] = ..., y_vel_sigma: _Optional[float] = ..., z_vel_sigma: _Optional[float] = ..., base_station_id: _Optional[str] = ..., velocity_latency: _Optional[float] = ..., diff_age: _Optional[float] = ..., solution_age: _Optional[float] = ..., num_satellites_tracked: _Optional[int] = ..., num_satellites_used_in_solution: _Optional[int] = ..., num_gps_and_glonass_l1_used_in_solution: _Optional[int] = ..., num_gps_and_glonass_l1_and_l2_used_in_solution: _Optional[int] = ..., extended_solution_status: _Optional[_Union[_novatel_extended_solution_status_pb2.NovatelExtendedSolutionStatus, _Mapping]] = ..., signal_mask: _Optional[_Union[_novatel_signal_mask_pb2.NovatelSignalMask, _Mapping]] = ...) -> None: ...
