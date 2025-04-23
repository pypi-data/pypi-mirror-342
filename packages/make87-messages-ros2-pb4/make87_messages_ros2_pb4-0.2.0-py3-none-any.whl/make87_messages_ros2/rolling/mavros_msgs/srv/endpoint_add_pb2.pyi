from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class EndpointAddRequest(_message.Message):
    __slots__ = ["url", "type"]
    URL_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    url: str
    type: int
    def __init__(self, url: _Optional[str] = ..., type: _Optional[int] = ...) -> None: ...

class EndpointAddResponse(_message.Message):
    __slots__ = ["successful", "reason", "id"]
    SUCCESSFUL_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    successful: bool
    reason: str
    id: int
    def __init__(self, successful: bool = ..., reason: _Optional[str] = ..., id: _Optional[int] = ...) -> None: ...
