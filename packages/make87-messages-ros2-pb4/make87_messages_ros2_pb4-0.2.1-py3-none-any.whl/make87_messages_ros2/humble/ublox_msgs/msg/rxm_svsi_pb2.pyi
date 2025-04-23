from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.ublox_msgs.msg import rxm_svsisv_pb2 as _rxm_svsisv_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RxmSVSI(_message.Message):
    __slots__ = ["header", "i_tow", "week", "num_vis", "num_sv", "sv"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    I_TOW_FIELD_NUMBER: _ClassVar[int]
    WEEK_FIELD_NUMBER: _ClassVar[int]
    NUM_VIS_FIELD_NUMBER: _ClassVar[int]
    NUM_SV_FIELD_NUMBER: _ClassVar[int]
    SV_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    i_tow: int
    week: int
    num_vis: int
    num_sv: int
    sv: _containers.RepeatedCompositeFieldContainer[_rxm_svsisv_pb2.RxmSVSISV]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., i_tow: _Optional[int] = ..., week: _Optional[int] = ..., num_vis: _Optional[int] = ..., num_sv: _Optional[int] = ..., sv: _Optional[_Iterable[_Union[_rxm_svsisv_pb2.RxmSVSISV, _Mapping]]] = ...) -> None: ...
