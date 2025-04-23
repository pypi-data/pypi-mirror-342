from make87_messages_ros2.jazzy.geometry_msgs.msg import point_pb2 as _point_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BoundingBoxQueryRequest(_message.Message):
    __slots__ = ["min", "max"]
    MIN_FIELD_NUMBER: _ClassVar[int]
    MAX_FIELD_NUMBER: _ClassVar[int]
    min: _point_pb2.Point
    max: _point_pb2.Point
    def __init__(self, min: _Optional[_Union[_point_pb2.Point, _Mapping]] = ..., max: _Optional[_Union[_point_pb2.Point, _Mapping]] = ...) -> None: ...

class BoundingBoxQueryResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
