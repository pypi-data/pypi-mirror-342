from make87_messages_ros2.jazzy.ur_dashboard_msgs.msg import program_state_pb2 as _program_state_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetProgramStateRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetProgramStateResponse(_message.Message):
    __slots__ = ["state", "program_name", "answer", "success"]
    STATE_FIELD_NUMBER: _ClassVar[int]
    PROGRAM_NAME_FIELD_NUMBER: _ClassVar[int]
    ANSWER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    state: _program_state_pb2.ProgramState
    program_name: str
    answer: str
    success: bool
    def __init__(self, state: _Optional[_Union[_program_state_pb2.ProgramState, _Mapping]] = ..., program_name: _Optional[str] = ..., answer: _Optional[str] = ..., success: bool = ...) -> None: ...
