from make87_messages_ros2.jazzy.nav_msgs.msg import occupancy_grid_pb2 as _occupancy_grid_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LoadMapRequest(_message.Message):
    __slots__ = ["map_url"]
    MAP_URL_FIELD_NUMBER: _ClassVar[int]
    map_url: str
    def __init__(self, map_url: _Optional[str] = ...) -> None: ...

class LoadMapResponse(_message.Message):
    __slots__ = ["map", "result"]
    MAP_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    map: _occupancy_grid_pb2.OccupancyGrid
    result: int
    def __init__(self, map: _Optional[_Union[_occupancy_grid_pb2.OccupancyGrid, _Mapping]] = ..., result: _Optional[int] = ...) -> None: ...
