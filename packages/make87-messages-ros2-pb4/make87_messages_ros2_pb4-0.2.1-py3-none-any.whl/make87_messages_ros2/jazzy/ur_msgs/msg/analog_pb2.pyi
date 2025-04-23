from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Analog(_message.Message):
    __slots__ = ["pin", "domain", "state"]
    PIN_FIELD_NUMBER: _ClassVar[int]
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    pin: int
    domain: int
    state: float
    def __init__(self, pin: _Optional[int] = ..., domain: _Optional[int] = ..., state: _Optional[float] = ...) -> None: ...
