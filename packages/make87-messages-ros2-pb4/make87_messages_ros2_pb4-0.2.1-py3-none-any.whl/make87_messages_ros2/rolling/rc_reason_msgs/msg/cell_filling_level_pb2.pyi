from make87_messages_ros2.rolling.geometry_msgs.msg import point_pb2 as _point_pb2
from make87_messages_ros2.rolling.rc_reason_msgs.msg import range_value_pb2 as _range_value_pb2
from make87_messages_ros2.rolling.rc_reason_msgs.msg import rectangle_pb2 as _rectangle_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CellFillingLevel(_message.Message):
    __slots__ = ["cell_size", "cell_position", "level_in_percent", "level_free_in_meters", "coverage"]
    CELL_SIZE_FIELD_NUMBER: _ClassVar[int]
    CELL_POSITION_FIELD_NUMBER: _ClassVar[int]
    LEVEL_IN_PERCENT_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FREE_IN_METERS_FIELD_NUMBER: _ClassVar[int]
    COVERAGE_FIELD_NUMBER: _ClassVar[int]
    cell_size: _rectangle_pb2.Rectangle
    cell_position: _point_pb2.Point
    level_in_percent: _range_value_pb2.RangeValue
    level_free_in_meters: _range_value_pb2.RangeValue
    coverage: float
    def __init__(self, cell_size: _Optional[_Union[_rectangle_pb2.Rectangle, _Mapping]] = ..., cell_position: _Optional[_Union[_point_pb2.Point, _Mapping]] = ..., level_in_percent: _Optional[_Union[_range_value_pb2.RangeValue, _Mapping]] = ..., level_free_in_meters: _Optional[_Union[_range_value_pb2.RangeValue, _Mapping]] = ..., coverage: _Optional[float] = ...) -> None: ...
