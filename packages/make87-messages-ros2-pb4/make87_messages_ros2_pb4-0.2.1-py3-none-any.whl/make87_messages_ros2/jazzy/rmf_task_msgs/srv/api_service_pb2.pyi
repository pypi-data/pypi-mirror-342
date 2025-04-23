from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ApiServiceRequest(_message.Message):
    __slots__ = ["json_msg"]
    JSON_MSG_FIELD_NUMBER: _ClassVar[int]
    json_msg: str
    def __init__(self, json_msg: _Optional[str] = ...) -> None: ...

class ApiServiceResponse(_message.Message):
    __slots__ = ["json_msg"]
    JSON_MSG_FIELD_NUMBER: _ClassVar[int]
    json_msg: str
    def __init__(self, json_msg: _Optional[str] = ...) -> None: ...
