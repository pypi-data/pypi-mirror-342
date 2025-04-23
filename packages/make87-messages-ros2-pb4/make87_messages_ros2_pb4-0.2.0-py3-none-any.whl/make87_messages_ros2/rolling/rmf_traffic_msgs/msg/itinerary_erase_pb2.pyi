from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ItineraryErase(_message.Message):
    __slots__ = ["participant", "routes", "itinerary_version"]
    PARTICIPANT_FIELD_NUMBER: _ClassVar[int]
    ROUTES_FIELD_NUMBER: _ClassVar[int]
    ITINERARY_VERSION_FIELD_NUMBER: _ClassVar[int]
    participant: int
    routes: _containers.RepeatedScalarFieldContainer[int]
    itinerary_version: int
    def __init__(self, participant: _Optional[int] = ..., routes: _Optional[_Iterable[int]] = ..., itinerary_version: _Optional[int] = ...) -> None: ...
