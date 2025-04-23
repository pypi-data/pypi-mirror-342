from make87_messages_ros2.jazzy.geometry_msgs.msg import polygon_pb2 as _polygon_pb2
from make87_messages_ros2.jazzy.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Shape(_message.Message):
    __slots__ = ["type", "footprint", "dimensions"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    FOOTPRINT_FIELD_NUMBER: _ClassVar[int]
    DIMENSIONS_FIELD_NUMBER: _ClassVar[int]
    type: int
    footprint: _polygon_pb2.Polygon
    dimensions: _vector3_pb2.Vector3
    def __init__(self, type: _Optional[int] = ..., footprint: _Optional[_Union[_polygon_pb2.Polygon, _Mapping]] = ..., dimensions: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ...) -> None: ...
