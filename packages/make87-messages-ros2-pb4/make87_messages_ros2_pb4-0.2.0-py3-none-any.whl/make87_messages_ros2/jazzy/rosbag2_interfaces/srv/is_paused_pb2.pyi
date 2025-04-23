from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class IsPausedRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class IsPausedResponse(_message.Message):
    __slots__ = ["paused"]
    PAUSED_FIELD_NUMBER: _ClassVar[int]
    paused: bool
    def __init__(self, paused: bool = ...) -> None: ...
