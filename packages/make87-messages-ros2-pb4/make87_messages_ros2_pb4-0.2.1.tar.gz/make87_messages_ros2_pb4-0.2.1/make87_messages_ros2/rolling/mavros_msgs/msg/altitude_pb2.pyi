from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Altitude(_message.Message):
    __slots__ = ["header", "monotonic", "amsl", "local", "relative", "terrain", "bottom_clearance"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MONOTONIC_FIELD_NUMBER: _ClassVar[int]
    AMSL_FIELD_NUMBER: _ClassVar[int]
    LOCAL_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_FIELD_NUMBER: _ClassVar[int]
    TERRAIN_FIELD_NUMBER: _ClassVar[int]
    BOTTOM_CLEARANCE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    monotonic: float
    amsl: float
    local: float
    relative: float
    terrain: float
    bottom_clearance: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., monotonic: _Optional[float] = ..., amsl: _Optional[float] = ..., local: _Optional[float] = ..., relative: _Optional[float] = ..., terrain: _Optional[float] = ..., bottom_clearance: _Optional[float] = ...) -> None: ...
