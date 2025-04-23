from make87_messages_ros2.rolling.builtin_interfaces.msg import duration_pb2 as _duration_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ADSBVehicle(_message.Message):
    __slots__ = ["header", "icao_address", "callsign", "latitude", "longitude", "altitude", "heading", "hor_velocity", "ver_velocity", "altitude_type", "emitter_type", "tslc", "flags", "squawk"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ICAO_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    CALLSIGN_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_FIELD_NUMBER: _ClassVar[int]
    HEADING_FIELD_NUMBER: _ClassVar[int]
    HOR_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    VER_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_TYPE_FIELD_NUMBER: _ClassVar[int]
    EMITTER_TYPE_FIELD_NUMBER: _ClassVar[int]
    TSLC_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    SQUAWK_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    icao_address: int
    callsign: str
    latitude: float
    longitude: float
    altitude: float
    heading: float
    hor_velocity: float
    ver_velocity: float
    altitude_type: int
    emitter_type: int
    tslc: _duration_pb2.Duration
    flags: int
    squawk: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., icao_address: _Optional[int] = ..., callsign: _Optional[str] = ..., latitude: _Optional[float] = ..., longitude: _Optional[float] = ..., altitude: _Optional[float] = ..., heading: _Optional[float] = ..., hor_velocity: _Optional[float] = ..., ver_velocity: _Optional[float] = ..., altitude_type: _Optional[int] = ..., emitter_type: _Optional[int] = ..., tslc: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., flags: _Optional[int] = ..., squawk: _Optional[int] = ...) -> None: ...
