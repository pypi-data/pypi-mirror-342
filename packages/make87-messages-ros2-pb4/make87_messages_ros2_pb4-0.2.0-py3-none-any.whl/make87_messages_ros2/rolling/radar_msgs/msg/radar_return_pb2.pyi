from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RadarReturn(_message.Message):
    __slots__ = ["range", "azimuth", "elevation", "doppler_velocity", "amplitude"]
    RANGE_FIELD_NUMBER: _ClassVar[int]
    AZIMUTH_FIELD_NUMBER: _ClassVar[int]
    ELEVATION_FIELD_NUMBER: _ClassVar[int]
    DOPPLER_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    AMPLITUDE_FIELD_NUMBER: _ClassVar[int]
    range: float
    azimuth: float
    elevation: float
    doppler_velocity: float
    amplitude: float
    def __init__(self, range: _Optional[float] = ..., azimuth: _Optional[float] = ..., elevation: _Optional[float] = ..., doppler_velocity: _Optional[float] = ..., amplitude: _Optional[float] = ...) -> None: ...
