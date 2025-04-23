from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ParamPushRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ParamPushResponse(_message.Message):
    __slots__ = ["success", "param_transfered"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    PARAM_TRANSFERED_FIELD_NUMBER: _ClassVar[int]
    success: bool
    param_transfered: int
    def __init__(self, success: bool = ..., param_transfered: _Optional[int] = ...) -> None: ...
