from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RslidarPacket(_message.Message):
    __slots__ = ["header", "is_difop", "is_frame_begin", "data"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    IS_DIFOP_FIELD_NUMBER: _ClassVar[int]
    IS_FRAME_BEGIN_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    is_difop: int
    is_frame_begin: int
    data: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., is_difop: _Optional[int] = ..., is_frame_begin: _Optional[int] = ..., data: _Optional[_Iterable[int]] = ...) -> None: ...
