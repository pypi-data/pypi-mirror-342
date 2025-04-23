from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DataPoint(_message.Message):
    __slots__ = ["header", "name_index", "stamp", "value"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NAME_INDEX_FIELD_NUMBER: _ClassVar[int]
    STAMP_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    name_index: int
    stamp: float
    value: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., name_index: _Optional[int] = ..., stamp: _Optional[float] = ..., value: _Optional[float] = ...) -> None: ...
