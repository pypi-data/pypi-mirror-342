from make87_messages_ros2.rolling.geometry_msgs.msg import transform_stamped_pb2 as _transform_stamped_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TFMessage(_message.Message):
    __slots__ = ["transforms"]
    TRANSFORMS_FIELD_NUMBER: _ClassVar[int]
    transforms: _containers.RepeatedCompositeFieldContainer[_transform_stamped_pb2.TransformStamped]
    def __init__(self, transforms: _Optional[_Iterable[_Union[_transform_stamped_pb2.TransformStamped, _Mapping]]] = ...) -> None: ...
