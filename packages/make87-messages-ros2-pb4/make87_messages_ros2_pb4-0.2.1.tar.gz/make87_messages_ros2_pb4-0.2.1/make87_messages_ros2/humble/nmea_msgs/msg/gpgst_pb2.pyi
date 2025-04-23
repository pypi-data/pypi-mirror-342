from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Gpgst(_message.Message):
    __slots__ = ["header", "ros2_header", "message_id", "utc_seconds", "rms", "semi_major_dev", "semi_minor_dev", "orientation", "lat_dev", "lon_dev", "alt_dev"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    UTC_SECONDS_FIELD_NUMBER: _ClassVar[int]
    RMS_FIELD_NUMBER: _ClassVar[int]
    SEMI_MAJOR_DEV_FIELD_NUMBER: _ClassVar[int]
    SEMI_MINOR_DEV_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    LAT_DEV_FIELD_NUMBER: _ClassVar[int]
    LON_DEV_FIELD_NUMBER: _ClassVar[int]
    ALT_DEV_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    message_id: str
    utc_seconds: float
    rms: float
    semi_major_dev: float
    semi_minor_dev: float
    orientation: float
    lat_dev: float
    lon_dev: float
    alt_dev: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., message_id: _Optional[str] = ..., utc_seconds: _Optional[float] = ..., rms: _Optional[float] = ..., semi_major_dev: _Optional[float] = ..., semi_minor_dev: _Optional[float] = ..., orientation: _Optional[float] = ..., lat_dev: _Optional[float] = ..., lon_dev: _Optional[float] = ..., alt_dev: _Optional[float] = ...) -> None: ...
