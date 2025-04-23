from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import point_pb2 as _point_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class InteractiveMarkerFeedback(_message.Message):
    __slots__ = ["header", "ros2_header", "client_id", "marker_name", "control_name", "event_type", "pose", "menu_entry_id", "mouse_point", "mouse_point_valid"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    CLIENT_ID_FIELD_NUMBER: _ClassVar[int]
    MARKER_NAME_FIELD_NUMBER: _ClassVar[int]
    CONTROL_NAME_FIELD_NUMBER: _ClassVar[int]
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    MENU_ENTRY_ID_FIELD_NUMBER: _ClassVar[int]
    MOUSE_POINT_FIELD_NUMBER: _ClassVar[int]
    MOUSE_POINT_VALID_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    client_id: str
    marker_name: str
    control_name: str
    event_type: int
    pose: _pose_pb2.Pose
    menu_entry_id: int
    mouse_point: _point_pb2.Point
    mouse_point_valid: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., client_id: _Optional[str] = ..., marker_name: _Optional[str] = ..., control_name: _Optional[str] = ..., event_type: _Optional[int] = ..., pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., menu_entry_id: _Optional[int] = ..., mouse_point: _Optional[_Union[_point_pb2.Point, _Mapping]] = ..., mouse_point_valid: bool = ...) -> None: ...
