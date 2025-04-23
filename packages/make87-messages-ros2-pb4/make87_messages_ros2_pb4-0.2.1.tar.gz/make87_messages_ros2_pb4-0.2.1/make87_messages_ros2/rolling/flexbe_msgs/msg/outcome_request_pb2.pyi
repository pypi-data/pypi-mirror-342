from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class OutcomeRequest(_message.Message):
    __slots__ = ["outcome", "target"]
    OUTCOME_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    outcome: int
    target: str
    def __init__(self, outcome: _Optional[int] = ..., target: _Optional[str] = ...) -> None: ...
