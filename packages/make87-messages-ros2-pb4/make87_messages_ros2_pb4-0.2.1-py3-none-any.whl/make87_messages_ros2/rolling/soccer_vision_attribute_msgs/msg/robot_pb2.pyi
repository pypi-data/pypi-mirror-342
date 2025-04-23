from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Robot(_message.Message):
    __slots__ = ["player_number", "team", "state", "facing"]
    PLAYER_NUMBER_FIELD_NUMBER: _ClassVar[int]
    TEAM_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    FACING_FIELD_NUMBER: _ClassVar[int]
    player_number: int
    team: int
    state: int
    facing: int
    def __init__(self, player_number: _Optional[int] = ..., team: _Optional[int] = ..., state: _Optional[int] = ..., facing: _Optional[int] = ...) -> None: ...
