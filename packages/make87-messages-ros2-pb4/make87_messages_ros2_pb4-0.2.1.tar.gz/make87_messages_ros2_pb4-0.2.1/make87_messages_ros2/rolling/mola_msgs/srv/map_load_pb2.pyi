from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class MapLoadRequest(_message.Message):
    __slots__ = ["map_path"]
    MAP_PATH_FIELD_NUMBER: _ClassVar[int]
    map_path: str
    def __init__(self, map_path: _Optional[str] = ...) -> None: ...

class MapLoadResponse(_message.Message):
    __slots__ = ["success", "error_message"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    error_message: str
    def __init__(self, success: bool = ..., error_message: _Optional[str] = ...) -> None: ...
