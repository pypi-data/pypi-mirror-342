from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class EsfRAWBlock(_message.Message):
    __slots__ = ["data", "s_t_tag"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    S_T_TAG_FIELD_NUMBER: _ClassVar[int]
    data: int
    s_t_tag: int
    def __init__(self, data: _Optional[int] = ..., s_t_tag: _Optional[int] = ...) -> None: ...
