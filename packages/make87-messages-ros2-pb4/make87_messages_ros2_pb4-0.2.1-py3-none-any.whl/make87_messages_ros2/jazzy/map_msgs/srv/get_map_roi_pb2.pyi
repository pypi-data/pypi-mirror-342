from make87_messages_ros2.jazzy.nav_msgs.msg import occupancy_grid_pb2 as _occupancy_grid_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetMapROIRequest(_message.Message):
    __slots__ = ["x", "y", "l_x", "l_y"]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    L_X_FIELD_NUMBER: _ClassVar[int]
    L_Y_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    l_x: float
    l_y: float
    def __init__(self, x: _Optional[float] = ..., y: _Optional[float] = ..., l_x: _Optional[float] = ..., l_y: _Optional[float] = ...) -> None: ...

class GetMapROIResponse(_message.Message):
    __slots__ = ["sub_map"]
    SUB_MAP_FIELD_NUMBER: _ClassVar[int]
    sub_map: _occupancy_grid_pb2.OccupancyGrid
    def __init__(self, sub_map: _Optional[_Union[_occupancy_grid_pb2.OccupancyGrid, _Mapping]] = ...) -> None: ...
