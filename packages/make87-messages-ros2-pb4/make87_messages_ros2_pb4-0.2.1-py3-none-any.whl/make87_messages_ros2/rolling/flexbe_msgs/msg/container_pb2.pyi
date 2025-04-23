from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Container(_message.Message):
    __slots__ = ["state_id", "path", "children", "outcomes", "transitions", "type", "autonomy"]
    STATE_ID_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    CHILDREN_FIELD_NUMBER: _ClassVar[int]
    OUTCOMES_FIELD_NUMBER: _ClassVar[int]
    TRANSITIONS_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    AUTONOMY_FIELD_NUMBER: _ClassVar[int]
    state_id: int
    path: str
    children: _containers.RepeatedScalarFieldContainer[str]
    outcomes: _containers.RepeatedScalarFieldContainer[str]
    transitions: _containers.RepeatedScalarFieldContainer[str]
    type: int
    autonomy: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, state_id: _Optional[int] = ..., path: _Optional[str] = ..., children: _Optional[_Iterable[str]] = ..., outcomes: _Optional[_Iterable[str]] = ..., transitions: _Optional[_Iterable[str]] = ..., type: _Optional[int] = ..., autonomy: _Optional[_Iterable[int]] = ...) -> None: ...
