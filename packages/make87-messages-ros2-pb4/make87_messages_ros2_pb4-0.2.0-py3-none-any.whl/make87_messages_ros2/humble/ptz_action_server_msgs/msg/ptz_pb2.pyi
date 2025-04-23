from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Ptz(_message.Message):
    __slots__ = ["header", "pan", "tilt", "zoom"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PAN_FIELD_NUMBER: _ClassVar[int]
    TILT_FIELD_NUMBER: _ClassVar[int]
    ZOOM_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    pan: float
    tilt: float
    zoom: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., pan: _Optional[float] = ..., tilt: _Optional[float] = ..., zoom: _Optional[float] = ...) -> None: ...
