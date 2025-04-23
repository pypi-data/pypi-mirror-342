from make87_messages_ros2.jazzy.rcss3d_agent_msgs.msg import spherical_pb2 as _spherical_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Goalpost(_message.Message):
    __slots__ = ["name", "top"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TOP_FIELD_NUMBER: _ClassVar[int]
    name: str
    top: _spherical_pb2.Spherical
    def __init__(self, name: _Optional[str] = ..., top: _Optional[_Union[_spherical_pb2.Spherical, _Mapping]] = ...) -> None: ...
