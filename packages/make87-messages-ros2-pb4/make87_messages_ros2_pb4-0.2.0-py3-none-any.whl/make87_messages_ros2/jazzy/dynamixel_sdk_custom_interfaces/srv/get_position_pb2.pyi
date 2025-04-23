from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GetPositionRequest(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class GetPositionResponse(_message.Message):
    __slots__ = ["position"]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    position: int
    def __init__(self, position: _Optional[int] = ...) -> None: ...
