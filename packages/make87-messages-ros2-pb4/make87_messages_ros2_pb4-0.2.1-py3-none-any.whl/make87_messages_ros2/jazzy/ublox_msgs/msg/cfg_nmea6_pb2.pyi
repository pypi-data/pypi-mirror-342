from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CfgNMEA6(_message.Message):
    __slots__ = ["filter", "version", "num_sv", "flags"]
    FILTER_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    NUM_SV_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    filter: int
    version: int
    num_sv: int
    flags: int
    def __init__(self, filter: _Optional[int] = ..., version: _Optional[int] = ..., num_sv: _Optional[int] = ..., flags: _Optional[int] = ...) -> None: ...
