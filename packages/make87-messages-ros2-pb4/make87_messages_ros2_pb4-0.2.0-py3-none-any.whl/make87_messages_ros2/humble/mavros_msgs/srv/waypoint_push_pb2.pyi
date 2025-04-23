from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.mavros_msgs.msg import waypoint_pb2 as _waypoint_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class WaypointPushRequest(_message.Message):
    __slots__ = ["header", "start_index", "waypoints"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    START_INDEX_FIELD_NUMBER: _ClassVar[int]
    WAYPOINTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    start_index: int
    waypoints: _containers.RepeatedCompositeFieldContainer[_waypoint_pb2.Waypoint]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., start_index: _Optional[int] = ..., waypoints: _Optional[_Iterable[_Union[_waypoint_pb2.Waypoint, _Mapping]]] = ...) -> None: ...

class WaypointPushResponse(_message.Message):
    __slots__ = ["header", "success", "wp_transfered"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    WP_TRANSFERED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    wp_transfered: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., wp_transfered: _Optional[int] = ...) -> None: ...
