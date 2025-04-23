from make87_messages_ros2.jazzy.geometry_msgs.msg import point_pb2 as _point_pb2
from make87_messages_ros2.jazzy.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ContactInformation(_message.Message):
    __slots__ = ["header", "position", "normal", "depth", "contact_body_1", "body_type_1", "contact_body_2", "body_type_2"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    NORMAL_FIELD_NUMBER: _ClassVar[int]
    DEPTH_FIELD_NUMBER: _ClassVar[int]
    CONTACT_BODY_1_FIELD_NUMBER: _ClassVar[int]
    BODY_TYPE_1_FIELD_NUMBER: _ClassVar[int]
    CONTACT_BODY_2_FIELD_NUMBER: _ClassVar[int]
    BODY_TYPE_2_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    position: _point_pb2.Point
    normal: _vector3_pb2.Vector3
    depth: float
    contact_body_1: str
    body_type_1: int
    contact_body_2: str
    body_type_2: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., position: _Optional[_Union[_point_pb2.Point, _Mapping]] = ..., normal: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., depth: _Optional[float] = ..., contact_body_1: _Optional[str] = ..., body_type_1: _Optional[int] = ..., contact_body_2: _Optional[str] = ..., body_type_2: _Optional[int] = ...) -> None: ...
