from make87_messages_ros2.rolling.rmf_task_msgs.msg import behavior_parameter_pb2 as _behavior_parameter_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Behavior(_message.Message):
    __slots__ = ["name", "parameters"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    name: str
    parameters: _containers.RepeatedCompositeFieldContainer[_behavior_parameter_pb2.BehaviorParameter]
    def __init__(self, name: _Optional[str] = ..., parameters: _Optional[_Iterable[_Union[_behavior_parameter_pb2.BehaviorParameter, _Mapping]]] = ...) -> None: ...
