from make87_messages_ros2.jazzy.septentrio_gnss_driver.msg import block_header_pb2 as _block_header_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VelCovCartesian(_message.Message):
    __slots__ = ["header", "block_header", "mode", "error", "cov_vxvx", "cov_vyvy", "cov_vzvz", "cov_dtdt", "cov_vxvy", "cov_vxvz", "cov_vxdt", "cov_vyvz", "cov_vydt", "cov_vzdt"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BLOCK_HEADER_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    COV_VXVX_FIELD_NUMBER: _ClassVar[int]
    COV_VYVY_FIELD_NUMBER: _ClassVar[int]
    COV_VZVZ_FIELD_NUMBER: _ClassVar[int]
    COV_DTDT_FIELD_NUMBER: _ClassVar[int]
    COV_VXVY_FIELD_NUMBER: _ClassVar[int]
    COV_VXVZ_FIELD_NUMBER: _ClassVar[int]
    COV_VXDT_FIELD_NUMBER: _ClassVar[int]
    COV_VYVZ_FIELD_NUMBER: _ClassVar[int]
    COV_VYDT_FIELD_NUMBER: _ClassVar[int]
    COV_VZDT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    block_header: _block_header_pb2.BlockHeader
    mode: int
    error: int
    cov_vxvx: float
    cov_vyvy: float
    cov_vzvz: float
    cov_dtdt: float
    cov_vxvy: float
    cov_vxvz: float
    cov_vxdt: float
    cov_vyvz: float
    cov_vydt: float
    cov_vzdt: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., block_header: _Optional[_Union[_block_header_pb2.BlockHeader, _Mapping]] = ..., mode: _Optional[int] = ..., error: _Optional[int] = ..., cov_vxvx: _Optional[float] = ..., cov_vyvy: _Optional[float] = ..., cov_vzvz: _Optional[float] = ..., cov_dtdt: _Optional[float] = ..., cov_vxvy: _Optional[float] = ..., cov_vxvz: _Optional[float] = ..., cov_vxdt: _Optional[float] = ..., cov_vyvz: _Optional[float] = ..., cov_vydt: _Optional[float] = ..., cov_vzdt: _Optional[float] = ...) -> None: ...
