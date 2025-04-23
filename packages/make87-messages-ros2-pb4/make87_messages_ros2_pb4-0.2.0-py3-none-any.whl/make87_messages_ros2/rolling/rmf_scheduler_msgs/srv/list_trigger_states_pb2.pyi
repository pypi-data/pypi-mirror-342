from make87_messages_ros2.rolling.rmf_scheduler_msgs.msg import trigger_state_pb2 as _trigger_state_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ListTriggerStatesRequest(_message.Message):
    __slots__ = ["modified_after"]
    MODIFIED_AFTER_FIELD_NUMBER: _ClassVar[int]
    modified_after: int
    def __init__(self, modified_after: _Optional[int] = ...) -> None: ...

class ListTriggerStatesResponse(_message.Message):
    __slots__ = ["success", "message", "triggers"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    TRIGGERS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    triggers: _containers.RepeatedCompositeFieldContainer[_trigger_state_pb2.TriggerState]
    def __init__(self, success: bool = ..., message: _Optional[str] = ..., triggers: _Optional[_Iterable[_Union[_trigger_state_pb2.TriggerState, _Mapping]]] = ...) -> None: ...
