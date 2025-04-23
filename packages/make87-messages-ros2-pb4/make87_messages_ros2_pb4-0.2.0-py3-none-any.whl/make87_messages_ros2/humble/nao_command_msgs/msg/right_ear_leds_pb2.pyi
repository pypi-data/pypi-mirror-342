from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RightEarLeds(_message.Message):
    __slots__ = ["header", "intensities"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    INTENSITIES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    intensities: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., intensities: _Optional[_Iterable[float]] = ...) -> None: ...
