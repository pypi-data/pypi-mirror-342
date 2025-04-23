from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class COData(_message.Message):
    __slots__ = ["index", "subindex", "data"]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    SUBINDEX_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    index: int
    subindex: int
    data: int
    def __init__(self, index: _Optional[int] = ..., subindex: _Optional[int] = ..., data: _Optional[int] = ...) -> None: ...
