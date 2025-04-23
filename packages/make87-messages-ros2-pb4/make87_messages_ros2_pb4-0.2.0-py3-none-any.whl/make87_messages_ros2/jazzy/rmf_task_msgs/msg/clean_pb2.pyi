from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Clean(_message.Message):
    __slots__ = ["start_waypoint"]
    START_WAYPOINT_FIELD_NUMBER: _ClassVar[int]
    start_waypoint: str
    def __init__(self, start_waypoint: _Optional[str] = ...) -> None: ...
