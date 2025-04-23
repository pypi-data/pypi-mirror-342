from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SonarImageData(_message.Message):
    __slots__ = ["is_bigendian", "dtype", "beam_count", "data"]
    IS_BIGENDIAN_FIELD_NUMBER: _ClassVar[int]
    DTYPE_FIELD_NUMBER: _ClassVar[int]
    BEAM_COUNT_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    is_bigendian: bool
    dtype: int
    beam_count: int
    data: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, is_bigendian: bool = ..., dtype: _Optional[int] = ..., beam_count: _Optional[int] = ..., data: _Optional[_Iterable[int]] = ...) -> None: ...
