from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MgaGAL(_message.Message):
    __slots__ = ["header", "type", "version", "svid", "reserved0", "iod_nav", "delta_n", "m0", "e", "sqrt_a", "omega0", "i0", "omega", "omega_dot", "i_dot", "cuc", "cus", "crc", "crs", "cic", "cis", "toe", "af0", "af1", "af2", "sisaindex_e1_e5b", "toc", "bgd_e1_e5b", "reserved1", "health_e1b", "data_validity_e1b", "health_e5b", "data_validity_e5b", "reserved2"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    SVID_FIELD_NUMBER: _ClassVar[int]
    RESERVED0_FIELD_NUMBER: _ClassVar[int]
    IOD_NAV_FIELD_NUMBER: _ClassVar[int]
    DELTA_N_FIELD_NUMBER: _ClassVar[int]
    M0_FIELD_NUMBER: _ClassVar[int]
    E_FIELD_NUMBER: _ClassVar[int]
    SQRT_A_FIELD_NUMBER: _ClassVar[int]
    OMEGA0_FIELD_NUMBER: _ClassVar[int]
    I0_FIELD_NUMBER: _ClassVar[int]
    OMEGA_FIELD_NUMBER: _ClassVar[int]
    OMEGA_DOT_FIELD_NUMBER: _ClassVar[int]
    I_DOT_FIELD_NUMBER: _ClassVar[int]
    CUC_FIELD_NUMBER: _ClassVar[int]
    CUS_FIELD_NUMBER: _ClassVar[int]
    CRC_FIELD_NUMBER: _ClassVar[int]
    CRS_FIELD_NUMBER: _ClassVar[int]
    CIC_FIELD_NUMBER: _ClassVar[int]
    CIS_FIELD_NUMBER: _ClassVar[int]
    TOE_FIELD_NUMBER: _ClassVar[int]
    AF0_FIELD_NUMBER: _ClassVar[int]
    AF1_FIELD_NUMBER: _ClassVar[int]
    AF2_FIELD_NUMBER: _ClassVar[int]
    SISAINDEX_E1_E5B_FIELD_NUMBER: _ClassVar[int]
    TOC_FIELD_NUMBER: _ClassVar[int]
    BGD_E1_E5B_FIELD_NUMBER: _ClassVar[int]
    RESERVED1_FIELD_NUMBER: _ClassVar[int]
    HEALTH_E1B_FIELD_NUMBER: _ClassVar[int]
    DATA_VALIDITY_E1B_FIELD_NUMBER: _ClassVar[int]
    HEALTH_E5B_FIELD_NUMBER: _ClassVar[int]
    DATA_VALIDITY_E5B_FIELD_NUMBER: _ClassVar[int]
    RESERVED2_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    type: int
    version: int
    svid: int
    reserved0: int
    iod_nav: int
    delta_n: int
    m0: int
    e: int
    sqrt_a: int
    omega0: int
    i0: int
    omega: int
    omega_dot: int
    i_dot: int
    cuc: int
    cus: int
    crc: int
    crs: int
    cic: int
    cis: int
    toe: int
    af0: int
    af1: int
    af2: int
    sisaindex_e1_e5b: int
    toc: int
    bgd_e1_e5b: int
    reserved1: _containers.RepeatedScalarFieldContainer[int]
    health_e1b: int
    data_validity_e1b: int
    health_e5b: int
    data_validity_e5b: int
    reserved2: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., type: _Optional[int] = ..., version: _Optional[int] = ..., svid: _Optional[int] = ..., reserved0: _Optional[int] = ..., iod_nav: _Optional[int] = ..., delta_n: _Optional[int] = ..., m0: _Optional[int] = ..., e: _Optional[int] = ..., sqrt_a: _Optional[int] = ..., omega0: _Optional[int] = ..., i0: _Optional[int] = ..., omega: _Optional[int] = ..., omega_dot: _Optional[int] = ..., i_dot: _Optional[int] = ..., cuc: _Optional[int] = ..., cus: _Optional[int] = ..., crc: _Optional[int] = ..., crs: _Optional[int] = ..., cic: _Optional[int] = ..., cis: _Optional[int] = ..., toe: _Optional[int] = ..., af0: _Optional[int] = ..., af1: _Optional[int] = ..., af2: _Optional[int] = ..., sisaindex_e1_e5b: _Optional[int] = ..., toc: _Optional[int] = ..., bgd_e1_e5b: _Optional[int] = ..., reserved1: _Optional[_Iterable[int]] = ..., health_e1b: _Optional[int] = ..., data_validity_e1b: _Optional[int] = ..., health_e5b: _Optional[int] = ..., data_validity_e5b: _Optional[int] = ..., reserved2: _Optional[_Iterable[int]] = ...) -> None: ...
