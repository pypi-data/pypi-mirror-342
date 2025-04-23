from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GameState(_message.Message):
    __slots__ = ["header", "time", "playmode", "score_left", "score_right"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    PLAYMODE_FIELD_NUMBER: _ClassVar[int]
    SCORE_LEFT_FIELD_NUMBER: _ClassVar[int]
    SCORE_RIGHT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    time: float
    playmode: str
    score_left: int
    score_right: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., time: _Optional[float] = ..., playmode: _Optional[str] = ..., score_left: _Optional[int] = ..., score_right: _Optional[int] = ...) -> None: ...
