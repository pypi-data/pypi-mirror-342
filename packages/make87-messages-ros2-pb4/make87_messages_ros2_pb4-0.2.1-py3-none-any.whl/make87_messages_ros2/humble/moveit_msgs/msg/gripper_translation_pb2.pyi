from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import vector3_stamped_pb2 as _vector3_stamped_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GripperTranslation(_message.Message):
    __slots__ = ["header", "direction", "desired_distance", "min_distance"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    DESIRED_DISTANCE_FIELD_NUMBER: _ClassVar[int]
    MIN_DISTANCE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    direction: _vector3_stamped_pb2.Vector3Stamped
    desired_distance: float
    min_distance: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., direction: _Optional[_Union[_vector3_stamped_pb2.Vector3Stamped, _Mapping]] = ..., desired_distance: _Optional[float] = ..., min_distance: _Optional[float] = ...) -> None: ...
