from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class BlockHeader(_message.Message):
    __slots__ = ["sync_1", "sync_2", "crc", "id", "revision", "length", "tow", "wnc"]
    SYNC_1_FIELD_NUMBER: _ClassVar[int]
    SYNC_2_FIELD_NUMBER: _ClassVar[int]
    CRC_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    REVISION_FIELD_NUMBER: _ClassVar[int]
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    TOW_FIELD_NUMBER: _ClassVar[int]
    WNC_FIELD_NUMBER: _ClassVar[int]
    sync_1: int
    sync_2: int
    crc: int
    id: int
    revision: int
    length: int
    tow: int
    wnc: int
    def __init__(self, sync_1: _Optional[int] = ..., sync_2: _Optional[int] = ..., crc: _Optional[int] = ..., id: _Optional[int] = ..., revision: _Optional[int] = ..., length: _Optional[int] = ..., tow: _Optional[int] = ..., wnc: _Optional[int] = ...) -> None: ...
