from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ClientMapVisualization(_message.Message):
    __slots__ = ["header", "timestamp", "visualization_id", "status", "distance_to_last_lc", "delay", "progress", "path_types"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    VISUALIZATION_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_TO_LAST_LC_FIELD_NUMBER: _ClassVar[int]
    DELAY_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_FIELD_NUMBER: _ClassVar[int]
    PATH_TYPES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    timestamp: _time_pb2.Time
    visualization_id: int
    status: int
    distance_to_last_lc: float
    delay: float
    progress: float
    path_types: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., timestamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., visualization_id: _Optional[int] = ..., status: _Optional[int] = ..., distance_to_last_lc: _Optional[float] = ..., delay: _Optional[float] = ..., progress: _Optional[float] = ..., path_types: _Optional[_Iterable[int]] = ...) -> None: ...
