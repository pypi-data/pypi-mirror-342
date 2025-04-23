from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BagfileProgress(_message.Message):
    __slots__ = ["header", "current_bagfile_name", "current_bagfile_id", "total_bagfiles", "total_messages", "processed_messages", "total_seconds", "processed_seconds"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CURRENT_BAGFILE_NAME_FIELD_NUMBER: _ClassVar[int]
    CURRENT_BAGFILE_ID_FIELD_NUMBER: _ClassVar[int]
    TOTAL_BAGFILES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    PROCESSED_MESSAGES_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SECONDS_FIELD_NUMBER: _ClassVar[int]
    PROCESSED_SECONDS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    current_bagfile_name: str
    current_bagfile_id: int
    total_bagfiles: int
    total_messages: int
    processed_messages: int
    total_seconds: float
    processed_seconds: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., current_bagfile_name: _Optional[str] = ..., current_bagfile_id: _Optional[int] = ..., total_bagfiles: _Optional[int] = ..., total_messages: _Optional[int] = ..., processed_messages: _Optional[int] = ..., total_seconds: _Optional[float] = ..., processed_seconds: _Optional[float] = ...) -> None: ...
