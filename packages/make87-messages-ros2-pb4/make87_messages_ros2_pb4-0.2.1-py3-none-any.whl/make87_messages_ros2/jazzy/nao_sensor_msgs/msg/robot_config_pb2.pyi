from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RobotConfig(_message.Message):
    __slots__ = ["body_id", "body_version", "head_id", "head_version"]
    BODY_ID_FIELD_NUMBER: _ClassVar[int]
    BODY_VERSION_FIELD_NUMBER: _ClassVar[int]
    HEAD_ID_FIELD_NUMBER: _ClassVar[int]
    HEAD_VERSION_FIELD_NUMBER: _ClassVar[int]
    body_id: str
    body_version: str
    head_id: str
    head_version: str
    def __init__(self, body_id: _Optional[str] = ..., body_version: _Optional[str] = ..., head_id: _Optional[str] = ..., head_version: _Optional[str] = ...) -> None: ...
