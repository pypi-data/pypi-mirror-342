from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class MonitoringCase(_message.Message):
    __slots__ = ["monitoring_case_number", "fields", "fields_valid"]
    MONITORING_CASE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    FIELDS_VALID_FIELD_NUMBER: _ClassVar[int]
    monitoring_case_number: int
    fields: _containers.RepeatedScalarFieldContainer[int]
    fields_valid: _containers.RepeatedScalarFieldContainer[bool]
    def __init__(self, monitoring_case_number: _Optional[int] = ..., fields: _Optional[_Iterable[int]] = ..., fields_valid: _Optional[_Iterable[bool]] = ...) -> None: ...
