from make87_messages_ros2.jazzy.moveit_msgs.msg import constraints_pb2 as _constraints_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TrajectoryConstraints(_message.Message):
    __slots__ = ["constraints"]
    CONSTRAINTS_FIELD_NUMBER: _ClassVar[int]
    constraints: _containers.RepeatedCompositeFieldContainer[_constraints_pb2.Constraints]
    def __init__(self, constraints: _Optional[_Iterable[_Union[_constraints_pb2.Constraints, _Mapping]]] = ...) -> None: ...
