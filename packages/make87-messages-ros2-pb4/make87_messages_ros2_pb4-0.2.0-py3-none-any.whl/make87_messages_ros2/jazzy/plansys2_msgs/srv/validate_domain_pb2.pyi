from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ValidateDomainRequest(_message.Message):
    __slots__ = ["domain"]
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    domain: str
    def __init__(self, domain: _Optional[str] = ...) -> None: ...

class ValidateDomainResponse(_message.Message):
    __slots__ = ["success", "error_info"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_INFO_FIELD_NUMBER: _ClassVar[int]
    success: bool
    error_info: str
    def __init__(self, success: bool = ..., error_info: _Optional[str] = ...) -> None: ...
