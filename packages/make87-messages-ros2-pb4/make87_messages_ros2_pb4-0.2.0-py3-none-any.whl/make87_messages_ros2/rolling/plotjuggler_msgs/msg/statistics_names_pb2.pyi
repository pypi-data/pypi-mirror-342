from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StatisticsNames(_message.Message):
    __slots__ = ["header", "names", "names_version"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NAMES_FIELD_NUMBER: _ClassVar[int]
    NAMES_VERSION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    names: _containers.RepeatedScalarFieldContainer[str]
    names_version: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., names: _Optional[_Iterable[str]] = ..., names_version: _Optional[int] = ...) -> None: ...
