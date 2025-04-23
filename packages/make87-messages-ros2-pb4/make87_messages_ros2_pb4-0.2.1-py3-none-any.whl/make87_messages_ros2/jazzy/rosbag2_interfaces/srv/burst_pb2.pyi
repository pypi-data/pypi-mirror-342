from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class BurstRequest(_message.Message):
    __slots__ = ["num_messages"]
    NUM_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    num_messages: int
    def __init__(self, num_messages: _Optional[int] = ...) -> None: ...

class BurstResponse(_message.Message):
    __slots__ = ["actually_burst"]
    ACTUALLY_BURST_FIELD_NUMBER: _ClassVar[int]
    actually_burst: int
    def __init__(self, actually_burst: _Optional[int] = ...) -> None: ...
