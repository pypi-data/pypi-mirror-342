from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.off_highway_uss_msgs.msg import echo_pb2 as _echo_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DirectEcho(_message.Message):
    __slots__ = ["header", "ros2_header", "id", "first", "first_filtered", "second"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    FIRST_FIELD_NUMBER: _ClassVar[int]
    FIRST_FILTERED_FIELD_NUMBER: _ClassVar[int]
    SECOND_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    id: int
    first: _echo_pb2.Echo
    first_filtered: _echo_pb2.Echo
    second: _echo_pb2.Echo
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., id: _Optional[int] = ..., first: _Optional[_Union[_echo_pb2.Echo, _Mapping]] = ..., first_filtered: _Optional[_Union[_echo_pb2.Echo, _Mapping]] = ..., second: _Optional[_Union[_echo_pb2.Echo, _Mapping]] = ...) -> None: ...
