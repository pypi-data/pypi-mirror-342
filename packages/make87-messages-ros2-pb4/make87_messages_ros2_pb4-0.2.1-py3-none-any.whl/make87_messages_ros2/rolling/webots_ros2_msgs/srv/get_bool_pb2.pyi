from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GetBoolRequest(_message.Message):
    __slots__ = ["ask"]
    ASK_FIELD_NUMBER: _ClassVar[int]
    ask: bool
    def __init__(self, ask: bool = ...) -> None: ...

class GetBoolResponse(_message.Message):
    __slots__ = ["value"]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: bool
    def __init__(self, value: bool = ...) -> None: ...
