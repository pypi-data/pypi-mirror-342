from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GPSINPUT(_message.Message):
    __slots__ = ["header", "ros2_header", "fix_type", "gps_id", "ignore_flags", "time_week_ms", "time_week", "lat", "lon", "alt", "hdop", "vdop", "vn", "ve", "vd", "speed_accuracy", "horiz_accuracy", "vert_accuracy", "satellites_visible", "yaw"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    FIX_TYPE_FIELD_NUMBER: _ClassVar[int]
    GPS_ID_FIELD_NUMBER: _ClassVar[int]
    IGNORE_FLAGS_FIELD_NUMBER: _ClassVar[int]
    TIME_WEEK_MS_FIELD_NUMBER: _ClassVar[int]
    TIME_WEEK_FIELD_NUMBER: _ClassVar[int]
    LAT_FIELD_NUMBER: _ClassVar[int]
    LON_FIELD_NUMBER: _ClassVar[int]
    ALT_FIELD_NUMBER: _ClassVar[int]
    HDOP_FIELD_NUMBER: _ClassVar[int]
    VDOP_FIELD_NUMBER: _ClassVar[int]
    VN_FIELD_NUMBER: _ClassVar[int]
    VE_FIELD_NUMBER: _ClassVar[int]
    VD_FIELD_NUMBER: _ClassVar[int]
    SPEED_ACCURACY_FIELD_NUMBER: _ClassVar[int]
    HORIZ_ACCURACY_FIELD_NUMBER: _ClassVar[int]
    VERT_ACCURACY_FIELD_NUMBER: _ClassVar[int]
    SATELLITES_VISIBLE_FIELD_NUMBER: _ClassVar[int]
    YAW_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    fix_type: int
    gps_id: int
    ignore_flags: int
    time_week_ms: int
    time_week: int
    lat: int
    lon: int
    alt: float
    hdop: float
    vdop: float
    vn: float
    ve: float
    vd: float
    speed_accuracy: float
    horiz_accuracy: float
    vert_accuracy: float
    satellites_visible: int
    yaw: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., fix_type: _Optional[int] = ..., gps_id: _Optional[int] = ..., ignore_flags: _Optional[int] = ..., time_week_ms: _Optional[int] = ..., time_week: _Optional[int] = ..., lat: _Optional[int] = ..., lon: _Optional[int] = ..., alt: _Optional[float] = ..., hdop: _Optional[float] = ..., vdop: _Optional[float] = ..., vn: _Optional[float] = ..., ve: _Optional[float] = ..., vd: _Optional[float] = ..., speed_accuracy: _Optional[float] = ..., horiz_accuracy: _Optional[float] = ..., vert_accuracy: _Optional[float] = ..., satellites_visible: _Optional[int] = ..., yaw: _Optional[int] = ...) -> None: ...
