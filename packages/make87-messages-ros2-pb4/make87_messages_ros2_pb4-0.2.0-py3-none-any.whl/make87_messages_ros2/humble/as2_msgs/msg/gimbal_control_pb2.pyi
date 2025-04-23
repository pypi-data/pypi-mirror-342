from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import vector3_stamped_pb2 as _vector3_stamped_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GimbalControl(_message.Message):
    __slots__ = ["header", "control_mode", "target"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CONTROL_MODE_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    control_mode: int
    target: _vector3_stamped_pb2.Vector3Stamped
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., control_mode: _Optional[int] = ..., target: _Optional[_Union[_vector3_stamped_pb2.Vector3Stamped, _Mapping]] = ...) -> None: ...
