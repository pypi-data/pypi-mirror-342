from make87_messages_ros2.rolling.sensor_msgs.msg import point_cloud2_pb2 as _point_cloud2_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetPointMapRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetPointMapResponse(_message.Message):
    __slots__ = ["map"]
    MAP_FIELD_NUMBER: _ClassVar[int]
    map: _point_cloud2_pb2.PointCloud2
    def __init__(self, map: _Optional[_Union[_point_cloud2_pb2.PointCloud2, _Mapping]] = ...) -> None: ...
