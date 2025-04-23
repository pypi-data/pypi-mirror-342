from make87_messages_ros2.rolling.geometry_msgs.msg import twist_pb2 as _twist_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TwistWithCovariance(_message.Message):
    __slots__ = ["twist", "covariance"]
    TWIST_FIELD_NUMBER: _ClassVar[int]
    COVARIANCE_FIELD_NUMBER: _ClassVar[int]
    twist: _twist_pb2.Twist
    covariance: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, twist: _Optional[_Union[_twist_pb2.Twist, _Mapping]] = ..., covariance: _Optional[_Iterable[float]] = ...) -> None: ...
