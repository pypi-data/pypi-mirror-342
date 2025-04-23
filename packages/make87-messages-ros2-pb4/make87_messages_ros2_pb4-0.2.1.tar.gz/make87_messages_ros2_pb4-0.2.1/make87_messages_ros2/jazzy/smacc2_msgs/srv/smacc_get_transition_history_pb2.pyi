from make87_messages_ros2.jazzy.smacc2_msgs.msg import smacc_transition_log_entry_pb2 as _smacc_transition_log_entry_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SmaccGetTransitionHistoryRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class SmaccGetTransitionHistoryResponse(_message.Message):
    __slots__ = ["history"]
    HISTORY_FIELD_NUMBER: _ClassVar[int]
    history: _containers.RepeatedCompositeFieldContainer[_smacc_transition_log_entry_pb2.SmaccTransitionLogEntry]
    def __init__(self, history: _Optional[_Iterable[_Union[_smacc_transition_log_entry_pb2.SmaccTransitionLogEntry, _Mapping]]] = ...) -> None: ...
