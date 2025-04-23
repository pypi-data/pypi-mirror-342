from make87_messages_ros2.jazzy.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from make87_messages_ros2.jazzy.visualization_msgs.msg import interactive_marker_control_pb2 as _interactive_marker_control_pb2
from make87_messages_ros2.jazzy.visualization_msgs.msg import menu_entry_pb2 as _menu_entry_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class InteractiveMarker(_message.Message):
    __slots__ = ["header", "pose", "name", "description", "scale", "menu_entries", "controls"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    SCALE_FIELD_NUMBER: _ClassVar[int]
    MENU_ENTRIES_FIELD_NUMBER: _ClassVar[int]
    CONTROLS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    pose: _pose_pb2.Pose
    name: str
    description: str
    scale: float
    menu_entries: _containers.RepeatedCompositeFieldContainer[_menu_entry_pb2.MenuEntry]
    controls: _containers.RepeatedCompositeFieldContainer[_interactive_marker_control_pb2.InteractiveMarkerControl]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., name: _Optional[str] = ..., description: _Optional[str] = ..., scale: _Optional[float] = ..., menu_entries: _Optional[_Iterable[_Union[_menu_entry_pb2.MenuEntry, _Mapping]]] = ..., controls: _Optional[_Iterable[_Union[_interactive_marker_control_pb2.InteractiveMarkerControl, _Mapping]]] = ...) -> None: ...
