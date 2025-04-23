from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Gpzda(_message.Message):
    __slots__ = ["header", "ros2_header", "message_id", "utc_seconds", "day", "month", "year", "hour_offset_gmt", "minute_offset_gmt"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    UTC_SECONDS_FIELD_NUMBER: _ClassVar[int]
    DAY_FIELD_NUMBER: _ClassVar[int]
    MONTH_FIELD_NUMBER: _ClassVar[int]
    YEAR_FIELD_NUMBER: _ClassVar[int]
    HOUR_OFFSET_GMT_FIELD_NUMBER: _ClassVar[int]
    MINUTE_OFFSET_GMT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    message_id: str
    utc_seconds: int
    day: int
    month: int
    year: int
    hour_offset_gmt: int
    minute_offset_gmt: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., message_id: _Optional[str] = ..., utc_seconds: _Optional[int] = ..., day: _Optional[int] = ..., month: _Optional[int] = ..., year: _Optional[int] = ..., hour_offset_gmt: _Optional[int] = ..., minute_offset_gmt: _Optional[int] = ...) -> None: ...
