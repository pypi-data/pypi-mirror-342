from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Confidence(_message.Message):
    __slots__ = ["confidence"]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    confidence: float
    def __init__(self, confidence: _Optional[float] = ...) -> None: ...
