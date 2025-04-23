from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SbgUtcTimeStatus(_message.Message):
    __slots__ = ["header", "clock_stable", "clock_status", "clock_utc_sync", "clock_utc_status"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CLOCK_STABLE_FIELD_NUMBER: _ClassVar[int]
    CLOCK_STATUS_FIELD_NUMBER: _ClassVar[int]
    CLOCK_UTC_SYNC_FIELD_NUMBER: _ClassVar[int]
    CLOCK_UTC_STATUS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    clock_stable: bool
    clock_status: int
    clock_utc_sync: bool
    clock_utc_status: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., clock_stable: bool = ..., clock_status: _Optional[int] = ..., clock_utc_sync: bool = ..., clock_utc_status: _Optional[int] = ...) -> None: ...
