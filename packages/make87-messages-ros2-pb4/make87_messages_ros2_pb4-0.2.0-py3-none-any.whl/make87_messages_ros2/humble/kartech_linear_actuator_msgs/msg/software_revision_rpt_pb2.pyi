from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SoftwareRevisionRpt(_message.Message):
    __slots__ = ["header", "ros2_header", "software_version_0", "software_version_1", "software_version_2", "software_day", "software_month_year"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    SOFTWARE_VERSION_0_FIELD_NUMBER: _ClassVar[int]
    SOFTWARE_VERSION_1_FIELD_NUMBER: _ClassVar[int]
    SOFTWARE_VERSION_2_FIELD_NUMBER: _ClassVar[int]
    SOFTWARE_DAY_FIELD_NUMBER: _ClassVar[int]
    SOFTWARE_MONTH_YEAR_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    software_version_0: int
    software_version_1: int
    software_version_2: int
    software_day: int
    software_month_year: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., software_version_0: _Optional[int] = ..., software_version_1: _Optional[int] = ..., software_version_2: _Optional[int] = ..., software_day: _Optional[int] = ..., software_month_year: _Optional[int] = ...) -> None: ...
