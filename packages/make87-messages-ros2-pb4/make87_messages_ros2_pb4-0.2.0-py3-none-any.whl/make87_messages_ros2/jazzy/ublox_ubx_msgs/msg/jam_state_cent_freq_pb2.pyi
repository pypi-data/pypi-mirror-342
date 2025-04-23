from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class JamStateCentFreq(_message.Message):
    __slots__ = ["cent_freq", "jammed"]
    CENT_FREQ_FIELD_NUMBER: _ClassVar[int]
    JAMMED_FIELD_NUMBER: _ClassVar[int]
    cent_freq: int
    jammed: bool
    def __init__(self, cent_freq: _Optional[int] = ..., jammed: bool = ...) -> None: ...
