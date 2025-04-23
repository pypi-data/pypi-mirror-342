from make87_messages_ros2.rolling.geometry_msgs.msg import polygon_pb2 as _polygon_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PolygonInstance(_message.Message):
    __slots__ = ["polygon", "id"]
    POLYGON_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    polygon: _polygon_pb2.Polygon
    id: int
    def __init__(self, polygon: _Optional[_Union[_polygon_pb2.Polygon, _Mapping]] = ..., id: _Optional[int] = ...) -> None: ...
