from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SetPenRequest(_message.Message):
    __slots__ = ["r", "g", "b", "width", "off"]
    R_FIELD_NUMBER: _ClassVar[int]
    G_FIELD_NUMBER: _ClassVar[int]
    B_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    OFF_FIELD_NUMBER: _ClassVar[int]
    r: int
    g: int
    b: int
    width: int
    off: int
    def __init__(self, r: _Optional[int] = ..., g: _Optional[int] = ..., b: _Optional[int] = ..., width: _Optional[int] = ..., off: _Optional[int] = ...) -> None: ...

class SetPenResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
