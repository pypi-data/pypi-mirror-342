from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class FileOpenRequest(_message.Message):
    __slots__ = ["file_path", "mode"]
    FILE_PATH_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    file_path: str
    mode: int
    def __init__(self, file_path: _Optional[str] = ..., mode: _Optional[int] = ...) -> None: ...

class FileOpenResponse(_message.Message):
    __slots__ = ["size", "success", "r_errno"]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    R_ERRNO_FIELD_NUMBER: _ClassVar[int]
    size: int
    success: bool
    r_errno: int
    def __init__(self, size: _Optional[int] = ..., success: bool = ..., r_errno: _Optional[int] = ...) -> None: ...
