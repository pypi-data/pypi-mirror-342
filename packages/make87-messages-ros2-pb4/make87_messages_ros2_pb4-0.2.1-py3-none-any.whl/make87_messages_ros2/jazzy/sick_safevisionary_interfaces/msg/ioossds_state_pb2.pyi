from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class IOOSSDSState(_message.Message):
    __slots__ = ["ossd1a", "ossd1b", "ossd2a", "ossd2b"]
    OSSD1A_FIELD_NUMBER: _ClassVar[int]
    OSSD1B_FIELD_NUMBER: _ClassVar[int]
    OSSD2A_FIELD_NUMBER: _ClassVar[int]
    OSSD2B_FIELD_NUMBER: _ClassVar[int]
    ossd1a: int
    ossd1b: int
    ossd2a: int
    ossd2b: int
    def __init__(self, ossd1a: _Optional[int] = ..., ossd1b: _Optional[int] = ..., ossd2a: _Optional[int] = ..., ossd2b: _Optional[int] = ...) -> None: ...
