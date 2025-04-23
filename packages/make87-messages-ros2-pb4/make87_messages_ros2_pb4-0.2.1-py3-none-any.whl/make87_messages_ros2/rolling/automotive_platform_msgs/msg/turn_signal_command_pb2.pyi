from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TurnSignalCommand(_message.Message):
    __slots__ = ["header", "mode", "turn_signal"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    TURN_SIGNAL_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    mode: int
    turn_signal: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., mode: _Optional[int] = ..., turn_signal: _Optional[int] = ...) -> None: ...
