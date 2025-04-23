from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class OrbAlmInfo(_message.Message):
    __slots__ = ["alm_usability", "alm_source"]
    ALM_USABILITY_FIELD_NUMBER: _ClassVar[int]
    ALM_SOURCE_FIELD_NUMBER: _ClassVar[int]
    alm_usability: int
    alm_source: int
    def __init__(self, alm_usability: _Optional[int] = ..., alm_source: _Optional[int] = ...) -> None: ...
