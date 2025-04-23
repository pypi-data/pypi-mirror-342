from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class NavSBASSV(_message.Message):
    __slots__ = ["svid", "flags", "udre", "sv_sys", "sv_service", "reserved1", "prc", "reserved2", "ic"]
    SVID_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    UDRE_FIELD_NUMBER: _ClassVar[int]
    SV_SYS_FIELD_NUMBER: _ClassVar[int]
    SV_SERVICE_FIELD_NUMBER: _ClassVar[int]
    RESERVED1_FIELD_NUMBER: _ClassVar[int]
    PRC_FIELD_NUMBER: _ClassVar[int]
    RESERVED2_FIELD_NUMBER: _ClassVar[int]
    IC_FIELD_NUMBER: _ClassVar[int]
    svid: int
    flags: int
    udre: int
    sv_sys: int
    sv_service: int
    reserved1: int
    prc: int
    reserved2: int
    ic: int
    def __init__(self, svid: _Optional[int] = ..., flags: _Optional[int] = ..., udre: _Optional[int] = ..., sv_sys: _Optional[int] = ..., sv_service: _Optional[int] = ..., reserved1: _Optional[int] = ..., prc: _Optional[int] = ..., reserved2: _Optional[int] = ..., ic: _Optional[int] = ...) -> None: ...
