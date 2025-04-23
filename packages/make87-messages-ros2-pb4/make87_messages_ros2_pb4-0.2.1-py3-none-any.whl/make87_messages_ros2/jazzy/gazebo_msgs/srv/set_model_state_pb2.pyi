from make87_messages_ros2.jazzy.gazebo_msgs.msg import model_state_pb2 as _model_state_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetModelStateRequest(_message.Message):
    __slots__ = ["model_state"]
    MODEL_STATE_FIELD_NUMBER: _ClassVar[int]
    model_state: _model_state_pb2.ModelState
    def __init__(self, model_state: _Optional[_Union[_model_state_pb2.ModelState, _Mapping]] = ...) -> None: ...

class SetModelStateResponse(_message.Message):
    __slots__ = ["success", "status_message"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    status_message: str
    def __init__(self, success: bool = ..., status_message: _Optional[str] = ...) -> None: ...
