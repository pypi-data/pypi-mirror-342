from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LaneletMapCellMetaData(_message.Message):
    __slots__ = ["header", "cell_id", "min_x", "max_x", "min_y", "max_y"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CELL_ID_FIELD_NUMBER: _ClassVar[int]
    MIN_X_FIELD_NUMBER: _ClassVar[int]
    MAX_X_FIELD_NUMBER: _ClassVar[int]
    MIN_Y_FIELD_NUMBER: _ClassVar[int]
    MAX_Y_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    cell_id: str
    min_x: float
    max_x: float
    min_y: float
    max_y: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., cell_id: _Optional[str] = ..., min_x: _Optional[float] = ..., max_x: _Optional[float] = ..., min_y: _Optional[float] = ..., max_y: _Optional[float] = ...) -> None: ...
