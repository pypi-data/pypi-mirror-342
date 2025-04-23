from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CommandHomeRequest(_message.Message):
    __slots__ = ["current_gps", "yaw", "latitude", "longitude", "altitude"]
    CURRENT_GPS_FIELD_NUMBER: _ClassVar[int]
    YAW_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_FIELD_NUMBER: _ClassVar[int]
    current_gps: bool
    yaw: float
    latitude: float
    longitude: float
    altitude: float
    def __init__(self, current_gps: bool = ..., yaw: _Optional[float] = ..., latitude: _Optional[float] = ..., longitude: _Optional[float] = ..., altitude: _Optional[float] = ...) -> None: ...

class CommandHomeResponse(_message.Message):
    __slots__ = ["success", "result"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    success: bool
    result: int
    def __init__(self, success: bool = ..., result: _Optional[int] = ...) -> None: ...
