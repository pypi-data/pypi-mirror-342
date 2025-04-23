from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class HistogramBucket(_message.Message):
    __slots__ = ["header", "bucket_boundary", "count"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BUCKET_BOUNDARY_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    bucket_boundary: float
    count: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., bucket_boundary: _Optional[float] = ..., count: _Optional[float] = ...) -> None: ...
