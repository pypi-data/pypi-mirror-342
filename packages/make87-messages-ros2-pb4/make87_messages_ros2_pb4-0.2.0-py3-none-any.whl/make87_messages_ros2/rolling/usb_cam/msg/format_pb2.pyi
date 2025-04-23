from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Format(_message.Message):
    __slots__ = ["pixel_format", "width", "height", "fps"]
    PIXEL_FORMAT_FIELD_NUMBER: _ClassVar[int]
    WIDTH_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    FPS_FIELD_NUMBER: _ClassVar[int]
    pixel_format: str
    width: int
    height: int
    fps: float
    def __init__(self, pixel_format: _Optional[str] = ..., width: _Optional[int] = ..., height: _Optional[int] = ..., fps: _Optional[float] = ...) -> None: ...
