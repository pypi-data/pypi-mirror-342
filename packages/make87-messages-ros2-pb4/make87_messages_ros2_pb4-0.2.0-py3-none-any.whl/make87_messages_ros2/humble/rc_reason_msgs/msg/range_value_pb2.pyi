from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RangeValue(_message.Message):
    __slots__ = ["header", "min", "max", "mean"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MIN_FIELD_NUMBER: _ClassVar[int]
    MAX_FIELD_NUMBER: _ClassVar[int]
    MEAN_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    min: float
    max: float
    mean: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., min: _Optional[float] = ..., max: _Optional[float] = ..., mean: _Optional[float] = ...) -> None: ...
