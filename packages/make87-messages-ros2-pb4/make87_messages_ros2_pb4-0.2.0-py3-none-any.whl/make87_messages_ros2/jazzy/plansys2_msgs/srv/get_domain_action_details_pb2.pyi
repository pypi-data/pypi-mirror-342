from make87_messages_ros2.jazzy.plansys2_msgs.msg import action_pb2 as _action_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetDomainActionDetailsRequest(_message.Message):
    __slots__ = ["action", "parameters"]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    action: str
    parameters: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, action: _Optional[str] = ..., parameters: _Optional[_Iterable[str]] = ...) -> None: ...

class GetDomainActionDetailsResponse(_message.Message):
    __slots__ = ["action", "success", "error_info"]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_INFO_FIELD_NUMBER: _ClassVar[int]
    action: _action_pb2.Action
    success: bool
    error_info: str
    def __init__(self, action: _Optional[_Union[_action_pb2.Action, _Mapping]] = ..., success: bool = ..., error_info: _Optional[str] = ...) -> None: ...
