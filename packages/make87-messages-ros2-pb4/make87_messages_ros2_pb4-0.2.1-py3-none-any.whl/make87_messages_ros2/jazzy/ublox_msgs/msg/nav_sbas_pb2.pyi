from make87_messages_ros2.jazzy.ublox_msgs.msg import nav_sbassv_pb2 as _nav_sbassv_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NavSBAS(_message.Message):
    __slots__ = ["i_tow", "geo", "mode", "sys", "service", "cnt", "reserved0", "sv"]
    I_TOW_FIELD_NUMBER: _ClassVar[int]
    GEO_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    SYS_FIELD_NUMBER: _ClassVar[int]
    SERVICE_FIELD_NUMBER: _ClassVar[int]
    CNT_FIELD_NUMBER: _ClassVar[int]
    RESERVED0_FIELD_NUMBER: _ClassVar[int]
    SV_FIELD_NUMBER: _ClassVar[int]
    i_tow: int
    geo: int
    mode: int
    sys: int
    service: int
    cnt: int
    reserved0: _containers.RepeatedScalarFieldContainer[int]
    sv: _containers.RepeatedCompositeFieldContainer[_nav_sbassv_pb2.NavSBASSV]
    def __init__(self, i_tow: _Optional[int] = ..., geo: _Optional[int] = ..., mode: _Optional[int] = ..., sys: _Optional[int] = ..., service: _Optional[int] = ..., cnt: _Optional[int] = ..., reserved0: _Optional[_Iterable[int]] = ..., sv: _Optional[_Iterable[_Union[_nav_sbassv_pb2.NavSBASSV, _Mapping]]] = ...) -> None: ...
