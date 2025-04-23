from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.grid_map_msgs.msg import grid_map_pb2 as _grid_map_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetGridMapRequest(_message.Message):
    __slots__ = ["header", "map"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MAP_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    map: _grid_map_pb2.GridMap
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., map: _Optional[_Union[_grid_map_pb2.GridMap, _Mapping]] = ...) -> None: ...

class SetGridMapResponse(_message.Message):
    __slots__ = ["header"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...
