from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CollisionDetectorState(_message.Message):
    __slots__ = ["polygons", "detections"]
    POLYGONS_FIELD_NUMBER: _ClassVar[int]
    DETECTIONS_FIELD_NUMBER: _ClassVar[int]
    polygons: _containers.RepeatedScalarFieldContainer[str]
    detections: _containers.RepeatedScalarFieldContainer[bool]
    def __init__(self, polygons: _Optional[_Iterable[str]] = ..., detections: _Optional[_Iterable[bool]] = ...) -> None: ...
