from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class NavVELECEF(_message.Message):
    __slots__ = ["i_tow", "ecef_vx", "ecef_vy", "ecef_vz", "s_acc"]
    I_TOW_FIELD_NUMBER: _ClassVar[int]
    ECEF_VX_FIELD_NUMBER: _ClassVar[int]
    ECEF_VY_FIELD_NUMBER: _ClassVar[int]
    ECEF_VZ_FIELD_NUMBER: _ClassVar[int]
    S_ACC_FIELD_NUMBER: _ClassVar[int]
    i_tow: int
    ecef_vx: int
    ecef_vy: int
    ecef_vz: int
    s_acc: int
    def __init__(self, i_tow: _Optional[int] = ..., ecef_vx: _Optional[int] = ..., ecef_vy: _Optional[int] = ..., ecef_vz: _Optional[int] = ..., s_acc: _Optional[int] = ...) -> None: ...
