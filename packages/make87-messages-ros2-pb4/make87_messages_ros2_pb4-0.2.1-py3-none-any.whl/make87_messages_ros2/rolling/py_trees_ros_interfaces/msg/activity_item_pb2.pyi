from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ActivityItem(_message.Message):
    __slots__ = ["key", "client_name", "activity_type", "previous_value", "current_value"]
    KEY_FIELD_NUMBER: _ClassVar[int]
    CLIENT_NAME_FIELD_NUMBER: _ClassVar[int]
    ACTIVITY_TYPE_FIELD_NUMBER: _ClassVar[int]
    PREVIOUS_VALUE_FIELD_NUMBER: _ClassVar[int]
    CURRENT_VALUE_FIELD_NUMBER: _ClassVar[int]
    key: str
    client_name: str
    activity_type: str
    previous_value: str
    current_value: str
    def __init__(self, key: _Optional[str] = ..., client_name: _Optional[str] = ..., activity_type: _Optional[str] = ..., previous_value: _Optional[str] = ..., current_value: _Optional[str] = ...) -> None: ...
