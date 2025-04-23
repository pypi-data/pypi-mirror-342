from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class HingeJointPos(_message.Message):
    __slots__ = ["name", "ax"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    AX_FIELD_NUMBER: _ClassVar[int]
    name: str
    ax: float
    def __init__(self, name: _Optional[str] = ..., ax: _Optional[float] = ...) -> None: ...
