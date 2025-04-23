from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SteerWheel(_message.Message):
    __slots__ = ["header", "mode", "angle", "angle_velocity"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    ANGLE_FIELD_NUMBER: _ClassVar[int]
    ANGLE_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    mode: int
    angle: float
    angle_velocity: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., mode: _Optional[int] = ..., angle: _Optional[float] = ..., angle_velocity: _Optional[float] = ...) -> None: ...
