from make87_messages_ros2.jazzy.irobot_create_msgs.msg import ir_intensity_pb2 as _ir_intensity_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class IrIntensityVector(_message.Message):
    __slots__ = ["header", "readings"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    READINGS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    readings: _containers.RepeatedCompositeFieldContainer[_ir_intensity_pb2.IrIntensity]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., readings: _Optional[_Iterable[_Union[_ir_intensity_pb2.IrIntensity, _Mapping]]] = ...) -> None: ...
