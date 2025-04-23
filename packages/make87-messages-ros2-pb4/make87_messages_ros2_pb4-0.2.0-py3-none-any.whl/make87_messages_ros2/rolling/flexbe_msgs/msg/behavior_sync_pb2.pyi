from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class BehaviorSync(_message.Message):
    __slots__ = ["behavior_id", "current_state_checksums"]
    BEHAVIOR_ID_FIELD_NUMBER: _ClassVar[int]
    CURRENT_STATE_CHECKSUMS_FIELD_NUMBER: _ClassVar[int]
    behavior_id: int
    current_state_checksums: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, behavior_id: _Optional[int] = ..., current_state_checksums: _Optional[_Iterable[int]] = ...) -> None: ...
