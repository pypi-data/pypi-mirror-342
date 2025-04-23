from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ServiceInfo(_message.Message):
    __slots__ = ["header", "name", "resolved_name", "description", "group", "message_type", "server", "topic_service"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    RESOLVED_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SERVER_FIELD_NUMBER: _ClassVar[int]
    TOPIC_SERVICE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    name: str
    resolved_name: str
    description: str
    group: str
    message_type: str
    server: bool
    topic_service: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., name: _Optional[str] = ..., resolved_name: _Optional[str] = ..., description: _Optional[str] = ..., group: _Optional[str] = ..., message_type: _Optional[str] = ..., server: bool = ..., topic_service: bool = ...) -> None: ...
