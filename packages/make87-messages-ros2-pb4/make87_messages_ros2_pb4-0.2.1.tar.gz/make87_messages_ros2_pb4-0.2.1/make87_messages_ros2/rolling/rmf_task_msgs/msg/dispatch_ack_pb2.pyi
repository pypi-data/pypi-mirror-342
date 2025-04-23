from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DispatchAck(_message.Message):
    __slots__ = ["dispatch_id", "success", "errors"]
    DISPATCH_ID_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    dispatch_id: int
    success: bool
    errors: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, dispatch_id: _Optional[int] = ..., success: bool = ..., errors: _Optional[_Iterable[str]] = ...) -> None: ...
