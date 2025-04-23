from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.sensor_msgs.msg import point_cloud2_pb2 as _point_cloud2_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetPointMapRequest(_message.Message):
    __slots__ = ["header"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...

class GetPointMapResponse(_message.Message):
    __slots__ = ["header", "map"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MAP_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    map: _point_cloud2_pb2.PointCloud2
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., map: _Optional[_Union[_point_cloud2_pb2.PointCloud2, _Mapping]] = ...) -> None: ...
