from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NavSOL(_message.Message):
    __slots__ = ["header", "i_tow", "f_tow", "week", "gps_fix", "flags", "ecef_x", "ecef_y", "ecef_z", "p_acc", "ecef_vx", "ecef_vy", "ecef_vz", "s_acc", "p_dop", "reserved1", "num_sv", "reserved2"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    I_TOW_FIELD_NUMBER: _ClassVar[int]
    F_TOW_FIELD_NUMBER: _ClassVar[int]
    WEEK_FIELD_NUMBER: _ClassVar[int]
    GPS_FIX_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    ECEF_X_FIELD_NUMBER: _ClassVar[int]
    ECEF_Y_FIELD_NUMBER: _ClassVar[int]
    ECEF_Z_FIELD_NUMBER: _ClassVar[int]
    P_ACC_FIELD_NUMBER: _ClassVar[int]
    ECEF_VX_FIELD_NUMBER: _ClassVar[int]
    ECEF_VY_FIELD_NUMBER: _ClassVar[int]
    ECEF_VZ_FIELD_NUMBER: _ClassVar[int]
    S_ACC_FIELD_NUMBER: _ClassVar[int]
    P_DOP_FIELD_NUMBER: _ClassVar[int]
    RESERVED1_FIELD_NUMBER: _ClassVar[int]
    NUM_SV_FIELD_NUMBER: _ClassVar[int]
    RESERVED2_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    i_tow: int
    f_tow: int
    week: int
    gps_fix: int
    flags: int
    ecef_x: int
    ecef_y: int
    ecef_z: int
    p_acc: int
    ecef_vx: int
    ecef_vy: int
    ecef_vz: int
    s_acc: int
    p_dop: int
    reserved1: int
    num_sv: int
    reserved2: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., i_tow: _Optional[int] = ..., f_tow: _Optional[int] = ..., week: _Optional[int] = ..., gps_fix: _Optional[int] = ..., flags: _Optional[int] = ..., ecef_x: _Optional[int] = ..., ecef_y: _Optional[int] = ..., ecef_z: _Optional[int] = ..., p_acc: _Optional[int] = ..., ecef_vx: _Optional[int] = ..., ecef_vy: _Optional[int] = ..., ecef_vz: _Optional[int] = ..., s_acc: _Optional[int] = ..., p_dop: _Optional[int] = ..., reserved1: _Optional[int] = ..., num_sv: _Optional[int] = ..., reserved2: _Optional[int] = ...) -> None: ...
