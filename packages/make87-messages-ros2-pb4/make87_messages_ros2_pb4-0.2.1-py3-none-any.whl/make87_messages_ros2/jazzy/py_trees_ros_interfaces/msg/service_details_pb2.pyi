from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ServiceDetails(_message.Message):
    __slots__ = ["service_name", "service_type"]
    SERVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    SERVICE_TYPE_FIELD_NUMBER: _ClassVar[int]
    service_name: str
    service_type: str
    def __init__(self, service_name: _Optional[str] = ..., service_type: _Optional[str] = ...) -> None: ...
