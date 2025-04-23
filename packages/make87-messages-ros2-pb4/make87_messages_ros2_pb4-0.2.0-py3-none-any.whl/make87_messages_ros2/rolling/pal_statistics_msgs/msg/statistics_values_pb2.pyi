from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StatisticsValues(_message.Message):
    __slots__ = ["header", "values", "names_version"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    VALUES_FIELD_NUMBER: _ClassVar[int]
    NAMES_VERSION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    values: _containers.RepeatedScalarFieldContainer[float]
    names_version: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., values: _Optional[_Iterable[float]] = ..., names_version: _Optional[int] = ...) -> None: ...
