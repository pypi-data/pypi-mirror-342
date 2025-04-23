from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ESCStatusItem(_message.Message):
    __slots__ = ["header", "rpm", "voltage", "current"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    RPM_FIELD_NUMBER: _ClassVar[int]
    VOLTAGE_FIELD_NUMBER: _ClassVar[int]
    CURRENT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    rpm: int
    voltage: float
    current: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., rpm: _Optional[int] = ..., voltage: _Optional[float] = ..., current: _Optional[float] = ...) -> None: ...
