from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class WaypointPullRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class WaypointPullResponse(_message.Message):
    __slots__ = ["success", "wp_received"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    WP_RECEIVED_FIELD_NUMBER: _ClassVar[int]
    success: bool
    wp_received: int
    def __init__(self, success: bool = ..., wp_received: _Optional[int] = ...) -> None: ...
