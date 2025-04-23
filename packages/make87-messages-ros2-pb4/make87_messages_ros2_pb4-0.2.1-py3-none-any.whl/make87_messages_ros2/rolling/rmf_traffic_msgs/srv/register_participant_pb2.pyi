from make87_messages_ros2.rolling.rmf_traffic_msgs.msg import participant_description_pb2 as _participant_description_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RegisterParticipantRequest(_message.Message):
    __slots__ = ["description"]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    description: _participant_description_pb2.ParticipantDescription
    def __init__(self, description: _Optional[_Union[_participant_description_pb2.ParticipantDescription, _Mapping]] = ...) -> None: ...

class RegisterParticipantResponse(_message.Message):
    __slots__ = ["participant_id", "last_itinerary_version", "last_plan_id", "next_storage_base", "error"]
    PARTICIPANT_ID_FIELD_NUMBER: _ClassVar[int]
    LAST_ITINERARY_VERSION_FIELD_NUMBER: _ClassVar[int]
    LAST_PLAN_ID_FIELD_NUMBER: _ClassVar[int]
    NEXT_STORAGE_BASE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    participant_id: int
    last_itinerary_version: int
    last_plan_id: int
    next_storage_base: int
    error: str
    def __init__(self, participant_id: _Optional[int] = ..., last_itinerary_version: _Optional[int] = ..., last_plan_id: _Optional[int] = ..., next_storage_base: _Optional[int] = ..., error: _Optional[str] = ...) -> None: ...
