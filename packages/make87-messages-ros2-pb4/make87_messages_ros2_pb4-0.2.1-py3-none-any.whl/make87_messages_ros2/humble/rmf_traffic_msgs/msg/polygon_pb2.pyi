from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rmf_traffic_msgs.msg import polygon_vertex_pb2 as _polygon_vertex_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Polygon(_message.Message):
    __slots__ = ["header", "vertices"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    VERTICES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    vertices: _containers.RepeatedCompositeFieldContainer[_polygon_vertex_pb2.PolygonVertex]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., vertices: _Optional[_Iterable[_Union[_polygon_vertex_pb2.PolygonVertex, _Mapping]]] = ...) -> None: ...
