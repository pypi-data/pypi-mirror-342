from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Hear(_message.Message):
    __slots__ = ["team", "time", "self", "direction", "message"]
    TEAM_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    SELF_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    team: str
    time: float
    self: bool
    direction: _containers.RepeatedScalarFieldContainer[float]
    message: str
    def __init__(self, team: _Optional[str] = ..., time: _Optional[float] = ..., self: bool = ..., direction: _Optional[_Iterable[float]] = ..., message: _Optional[str] = ...) -> None: ...
