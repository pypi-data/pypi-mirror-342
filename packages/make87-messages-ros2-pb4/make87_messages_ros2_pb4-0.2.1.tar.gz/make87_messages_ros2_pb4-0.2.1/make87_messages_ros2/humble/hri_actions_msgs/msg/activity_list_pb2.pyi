from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ActivityList(_message.Message):
    __slots__ = ["header", "activities_array"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ACTIVITIES_ARRAY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    activities_array: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., activities_array: _Optional[_Iterable[str]] = ...) -> None: ...
