from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Gpgsa(_message.Message):
    __slots__ = ["header", "message_id", "auto_manual_mode", "fix_mode", "sv_ids", "pdop", "hdop", "vdop"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    AUTO_MANUAL_MODE_FIELD_NUMBER: _ClassVar[int]
    FIX_MODE_FIELD_NUMBER: _ClassVar[int]
    SV_IDS_FIELD_NUMBER: _ClassVar[int]
    PDOP_FIELD_NUMBER: _ClassVar[int]
    HDOP_FIELD_NUMBER: _ClassVar[int]
    VDOP_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    message_id: str
    auto_manual_mode: str
    fix_mode: int
    sv_ids: _containers.RepeatedScalarFieldContainer[int]
    pdop: float
    hdop: float
    vdop: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., message_id: _Optional[str] = ..., auto_manual_mode: _Optional[str] = ..., fix_mode: _Optional[int] = ..., sv_ids: _Optional[_Iterable[int]] = ..., pdop: _Optional[float] = ..., hdop: _Optional[float] = ..., vdop: _Optional[float] = ...) -> None: ...
