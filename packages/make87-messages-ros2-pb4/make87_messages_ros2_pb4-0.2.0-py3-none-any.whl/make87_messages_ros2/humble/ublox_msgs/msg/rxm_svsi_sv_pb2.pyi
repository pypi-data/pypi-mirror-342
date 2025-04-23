from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RxmSVSI_SV(_message.Message):
    __slots__ = ["header", "svid", "svFlag", "azim", "elev", "age"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SVID_FIELD_NUMBER: _ClassVar[int]
    SVFLAG_FIELD_NUMBER: _ClassVar[int]
    AZIM_FIELD_NUMBER: _ClassVar[int]
    ELEV_FIELD_NUMBER: _ClassVar[int]
    AGE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    svid: int
    svFlag: int
    azim: int
    elev: int
    age: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., svid: _Optional[int] = ..., svFlag: _Optional[int] = ..., azim: _Optional[int] = ..., elev: _Optional[int] = ..., age: _Optional[int] = ...) -> None: ...
