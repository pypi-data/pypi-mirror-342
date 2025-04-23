from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NavVELECEF(_message.Message):
    __slots__ = ["header", "i_tow", "ecef_vx", "ecef_vy", "ecef_vz", "s_acc"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    I_TOW_FIELD_NUMBER: _ClassVar[int]
    ECEF_VX_FIELD_NUMBER: _ClassVar[int]
    ECEF_VY_FIELD_NUMBER: _ClassVar[int]
    ECEF_VZ_FIELD_NUMBER: _ClassVar[int]
    S_ACC_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    i_tow: int
    ecef_vx: int
    ecef_vy: int
    ecef_vz: int
    s_acc: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., i_tow: _Optional[int] = ..., ecef_vx: _Optional[int] = ..., ecef_vy: _Optional[int] = ..., ecef_vz: _Optional[int] = ..., s_acc: _Optional[int] = ...) -> None: ...
