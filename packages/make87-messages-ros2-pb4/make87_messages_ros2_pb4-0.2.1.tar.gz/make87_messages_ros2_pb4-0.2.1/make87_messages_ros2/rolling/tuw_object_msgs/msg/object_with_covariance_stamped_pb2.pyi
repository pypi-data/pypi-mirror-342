from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from make87_messages_ros2.rolling.tuw_object_msgs.msg import object_with_covariance_pb2 as _object_with_covariance_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ObjectWithCovarianceStamped(_message.Message):
    __slots__ = ["header", "object"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    OBJECT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    object: _object_with_covariance_pb2.ObjectWithCovariance
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., object: _Optional[_Union[_object_with_covariance_pb2.ObjectWithCovariance, _Mapping]] = ...) -> None: ...
