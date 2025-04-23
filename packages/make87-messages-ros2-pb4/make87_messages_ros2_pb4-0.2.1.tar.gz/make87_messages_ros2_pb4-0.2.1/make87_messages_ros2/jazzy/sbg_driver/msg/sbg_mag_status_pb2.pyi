from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SbgMagStatus(_message.Message):
    __slots__ = ["mag_x", "mag_y", "mag_z", "accel_x", "accel_y", "accel_z", "mags_in_range", "accels_in_range", "calibration"]
    MAG_X_FIELD_NUMBER: _ClassVar[int]
    MAG_Y_FIELD_NUMBER: _ClassVar[int]
    MAG_Z_FIELD_NUMBER: _ClassVar[int]
    ACCEL_X_FIELD_NUMBER: _ClassVar[int]
    ACCEL_Y_FIELD_NUMBER: _ClassVar[int]
    ACCEL_Z_FIELD_NUMBER: _ClassVar[int]
    MAGS_IN_RANGE_FIELD_NUMBER: _ClassVar[int]
    ACCELS_IN_RANGE_FIELD_NUMBER: _ClassVar[int]
    CALIBRATION_FIELD_NUMBER: _ClassVar[int]
    mag_x: bool
    mag_y: bool
    mag_z: bool
    accel_x: bool
    accel_y: bool
    accel_z: bool
    mags_in_range: bool
    accels_in_range: bool
    calibration: bool
    def __init__(self, mag_x: bool = ..., mag_y: bool = ..., mag_z: bool = ..., accel_x: bool = ..., accel_y: bool = ..., accel_z: bool = ..., mags_in_range: bool = ..., accels_in_range: bool = ..., calibration: bool = ...) -> None: ...
