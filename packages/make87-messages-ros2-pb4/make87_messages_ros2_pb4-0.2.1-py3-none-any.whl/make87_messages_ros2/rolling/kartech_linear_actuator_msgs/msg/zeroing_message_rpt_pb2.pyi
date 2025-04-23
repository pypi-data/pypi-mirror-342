from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ZeroingMessageRpt(_message.Message):
    __slots__ = ["header", "chip_1_voltage", "chip_2_voltage", "chip_error_1", "chip_error_2"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CHIP_1_VOLTAGE_FIELD_NUMBER: _ClassVar[int]
    CHIP_2_VOLTAGE_FIELD_NUMBER: _ClassVar[int]
    CHIP_ERROR_1_FIELD_NUMBER: _ClassVar[int]
    CHIP_ERROR_2_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    chip_1_voltage: int
    chip_2_voltage: int
    chip_error_1: int
    chip_error_2: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., chip_1_voltage: _Optional[int] = ..., chip_2_voltage: _Optional[int] = ..., chip_error_1: _Optional[int] = ..., chip_error_2: _Optional[int] = ...) -> None: ...
