from make87_messages_ros2.jazzy.rmf_traffic_msgs.msg import route_pb2 as _route_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ItineraryExtend(_message.Message):
    __slots__ = ["participant", "routes", "itinerary_version"]
    PARTICIPANT_FIELD_NUMBER: _ClassVar[int]
    ROUTES_FIELD_NUMBER: _ClassVar[int]
    ITINERARY_VERSION_FIELD_NUMBER: _ClassVar[int]
    participant: int
    routes: _containers.RepeatedCompositeFieldContainer[_route_pb2.Route]
    itinerary_version: int
    def __init__(self, participant: _Optional[int] = ..., routes: _Optional[_Iterable[_Union[_route_pb2.Route, _Mapping]]] = ..., itinerary_version: _Optional[int] = ...) -> None: ...
