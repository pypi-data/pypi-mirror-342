from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import point_pb2 as _point_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LaneBoundary(_message.Message):
    __slots__ = ["header", "style", "color", "line"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    STYLE_FIELD_NUMBER: _ClassVar[int]
    COLOR_FIELD_NUMBER: _ClassVar[int]
    LINE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    style: int
    color: int
    line: _containers.RepeatedCompositeFieldContainer[_point_pb2.Point]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., style: _Optional[int] = ..., color: _Optional[int] = ..., line: _Optional[_Iterable[_Union[_point_pb2.Point, _Mapping]]] = ...) -> None: ...
