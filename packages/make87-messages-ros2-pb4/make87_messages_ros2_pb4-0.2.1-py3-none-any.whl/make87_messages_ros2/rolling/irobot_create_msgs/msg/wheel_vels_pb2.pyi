from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class WheelVels(_message.Message):
    __slots__ = ["header", "velocity_left", "velocity_right"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_LEFT_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_RIGHT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    velocity_left: float
    velocity_right: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., velocity_left: _Optional[float] = ..., velocity_right: _Optional[float] = ...) -> None: ...
