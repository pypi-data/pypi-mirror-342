from make87_messages_ros2.jazzy.automotive_navigation_msgs.msg import lane_boundary_pb2 as _lane_boundary_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LaneBoundaryArray(_message.Message):
    __slots__ = ["boundaries"]
    BOUNDARIES_FIELD_NUMBER: _ClassVar[int]
    boundaries: _containers.RepeatedCompositeFieldContainer[_lane_boundary_pb2.LaneBoundary]
    def __init__(self, boundaries: _Optional[_Iterable[_Union[_lane_boundary_pb2.LaneBoundary, _Mapping]]] = ...) -> None: ...
