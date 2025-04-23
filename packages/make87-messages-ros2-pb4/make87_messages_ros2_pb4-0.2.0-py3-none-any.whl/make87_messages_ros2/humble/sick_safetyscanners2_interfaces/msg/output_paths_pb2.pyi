from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OutputPaths(_message.Message):
    __slots__ = ["header", "status", "is_safe", "is_valid", "active_monitoring_case"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    IS_SAFE_FIELD_NUMBER: _ClassVar[int]
    IS_VALID_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_MONITORING_CASE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    status: _containers.RepeatedScalarFieldContainer[bool]
    is_safe: _containers.RepeatedScalarFieldContainer[bool]
    is_valid: _containers.RepeatedScalarFieldContainer[bool]
    active_monitoring_case: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., status: _Optional[_Iterable[bool]] = ..., is_safe: _Optional[_Iterable[bool]] = ..., is_valid: _Optional[_Iterable[bool]] = ..., active_monitoring_case: _Optional[int] = ...) -> None: ...
