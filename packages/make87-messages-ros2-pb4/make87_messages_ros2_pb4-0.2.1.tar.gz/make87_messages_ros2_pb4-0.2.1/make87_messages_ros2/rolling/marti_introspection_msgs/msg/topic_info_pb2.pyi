from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class TopicInfo(_message.Message):
    __slots__ = ["name", "resolved_name", "description", "group", "message_type", "advertised"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    RESOLVED_NAME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_TYPE_FIELD_NUMBER: _ClassVar[int]
    ADVERTISED_FIELD_NUMBER: _ClassVar[int]
    name: str
    resolved_name: str
    description: str
    group: str
    message_type: str
    advertised: bool
    def __init__(self, name: _Optional[str] = ..., resolved_name: _Optional[str] = ..., description: _Optional[str] = ..., group: _Optional[str] = ..., message_type: _Optional[str] = ..., advertised: bool = ...) -> None: ...
