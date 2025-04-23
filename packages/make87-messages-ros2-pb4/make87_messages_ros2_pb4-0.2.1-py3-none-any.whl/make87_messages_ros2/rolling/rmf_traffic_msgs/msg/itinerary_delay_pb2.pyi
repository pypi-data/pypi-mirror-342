from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ItineraryDelay(_message.Message):
    __slots__ = ["participant", "delay", "itinerary_version"]
    PARTICIPANT_FIELD_NUMBER: _ClassVar[int]
    DELAY_FIELD_NUMBER: _ClassVar[int]
    ITINERARY_VERSION_FIELD_NUMBER: _ClassVar[int]
    participant: int
    delay: int
    itinerary_version: int
    def __init__(self, participant: _Optional[int] = ..., delay: _Optional[int] = ..., itinerary_version: _Optional[int] = ...) -> None: ...
