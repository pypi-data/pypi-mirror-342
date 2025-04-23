from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RangeInformation(_message.Message):
    __slots__ = ["header", "prn_number", "glofreq", "psr", "psr_std", "adr", "adr_std", "dopp", "noise_density_ratio", "locktime", "tracking_status"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PRN_NUMBER_FIELD_NUMBER: _ClassVar[int]
    GLOFREQ_FIELD_NUMBER: _ClassVar[int]
    PSR_FIELD_NUMBER: _ClassVar[int]
    PSR_STD_FIELD_NUMBER: _ClassVar[int]
    ADR_FIELD_NUMBER: _ClassVar[int]
    ADR_STD_FIELD_NUMBER: _ClassVar[int]
    DOPP_FIELD_NUMBER: _ClassVar[int]
    NOISE_DENSITY_RATIO_FIELD_NUMBER: _ClassVar[int]
    LOCKTIME_FIELD_NUMBER: _ClassVar[int]
    TRACKING_STATUS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    prn_number: int
    glofreq: int
    psr: float
    psr_std: float
    adr: float
    adr_std: float
    dopp: float
    noise_density_ratio: float
    locktime: float
    tracking_status: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., prn_number: _Optional[int] = ..., glofreq: _Optional[int] = ..., psr: _Optional[float] = ..., psr_std: _Optional[float] = ..., adr: _Optional[float] = ..., adr_std: _Optional[float] = ..., dopp: _Optional[float] = ..., noise_density_ratio: _Optional[float] = ..., locktime: _Optional[float] = ..., tracking_status: _Optional[int] = ...) -> None: ...
