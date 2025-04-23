from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ConfigureOutputsKdFreqDeadbandCmd(_message.Message):
    __slots__ = ["header", "confirm", "kd", "closed_loop_freq", "error_dead_band"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CONFIRM_FIELD_NUMBER: _ClassVar[int]
    KD_FIELD_NUMBER: _ClassVar[int]
    CLOSED_LOOP_FREQ_FIELD_NUMBER: _ClassVar[int]
    ERROR_DEAD_BAND_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    confirm: bool
    kd: int
    closed_loop_freq: int
    error_dead_band: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., confirm: bool = ..., kd: _Optional[int] = ..., closed_loop_freq: _Optional[int] = ..., error_dead_band: _Optional[float] = ...) -> None: ...
