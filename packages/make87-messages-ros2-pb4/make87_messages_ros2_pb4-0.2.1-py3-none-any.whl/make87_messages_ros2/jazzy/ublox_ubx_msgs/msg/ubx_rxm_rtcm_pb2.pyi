from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UBXRxmRTCM(_message.Message):
    __slots__ = ["header", "version", "crc_failed", "msg_used", "sub_type", "ref_station", "msg_type"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    CRC_FAILED_FIELD_NUMBER: _ClassVar[int]
    MSG_USED_FIELD_NUMBER: _ClassVar[int]
    SUB_TYPE_FIELD_NUMBER: _ClassVar[int]
    REF_STATION_FIELD_NUMBER: _ClassVar[int]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    version: int
    crc_failed: bool
    msg_used: int
    sub_type: int
    ref_station: int
    msg_type: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., version: _Optional[int] = ..., crc_failed: bool = ..., msg_used: _Optional[int] = ..., sub_type: _Optional[int] = ..., ref_station: _Optional[int] = ..., msg_type: _Optional[int] = ...) -> None: ...
