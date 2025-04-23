from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SCdevicestateSrvRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class SCdevicestateSrvResponse(_message.Message):
    __slots__ = ["state", "success"]
    STATE_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    state: int
    success: bool
    def __init__(self, state: _Optional[int] = ..., success: bool = ...) -> None: ...
