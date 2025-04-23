from make87_messages_ros2.rolling.map_msgs.msg import projected_map_info_pb2 as _projected_map_info_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProjectedMapsInfoRequest(_message.Message):
    __slots__ = ["projected_maps_info"]
    PROJECTED_MAPS_INFO_FIELD_NUMBER: _ClassVar[int]
    projected_maps_info: _containers.RepeatedCompositeFieldContainer[_projected_map_info_pb2.ProjectedMapInfo]
    def __init__(self, projected_maps_info: _Optional[_Iterable[_Union[_projected_map_info_pb2.ProjectedMapInfo, _Mapping]]] = ...) -> None: ...

class ProjectedMapsInfoResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
