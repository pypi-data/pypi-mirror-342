from make87_messages_ros2.rolling.flexbe_msgs.msg import container_pb2 as _container_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ContainerStructure(_message.Message):
    __slots__ = ["behavior_id", "containers"]
    BEHAVIOR_ID_FIELD_NUMBER: _ClassVar[int]
    CONTAINERS_FIELD_NUMBER: _ClassVar[int]
    behavior_id: int
    containers: _containers.RepeatedCompositeFieldContainer[_container_pb2.Container]
    def __init__(self, behavior_id: _Optional[int] = ..., containers: _Optional[_Iterable[_Union[_container_pb2.Container, _Mapping]]] = ...) -> None: ...
