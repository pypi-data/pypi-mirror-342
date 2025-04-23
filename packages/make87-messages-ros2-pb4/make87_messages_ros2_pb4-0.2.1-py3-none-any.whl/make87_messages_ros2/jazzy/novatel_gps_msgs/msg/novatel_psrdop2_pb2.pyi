from make87_messages_ros2.jazzy.novatel_gps_msgs.msg import novatel_message_header_pb2 as _novatel_message_header_pb2
from make87_messages_ros2.jazzy.novatel_gps_msgs.msg import novatel_psrdop2_system_pb2 as _novatel_psrdop2_system_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NovatelPsrdop2(_message.Message):
    __slots__ = ["header", "novatel_msg_header", "gdop", "pdop", "hdop", "vdop", "systems"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NOVATEL_MSG_HEADER_FIELD_NUMBER: _ClassVar[int]
    GDOP_FIELD_NUMBER: _ClassVar[int]
    PDOP_FIELD_NUMBER: _ClassVar[int]
    HDOP_FIELD_NUMBER: _ClassVar[int]
    VDOP_FIELD_NUMBER: _ClassVar[int]
    SYSTEMS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    novatel_msg_header: _novatel_message_header_pb2.NovatelMessageHeader
    gdop: float
    pdop: float
    hdop: float
    vdop: float
    systems: _containers.RepeatedCompositeFieldContainer[_novatel_psrdop2_system_pb2.NovatelPsrdop2System]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., novatel_msg_header: _Optional[_Union[_novatel_message_header_pb2.NovatelMessageHeader, _Mapping]] = ..., gdop: _Optional[float] = ..., pdop: _Optional[float] = ..., hdop: _Optional[float] = ..., vdop: _Optional[float] = ..., systems: _Optional[_Iterable[_Union[_novatel_psrdop2_system_pb2.NovatelPsrdop2System, _Mapping]]] = ...) -> None: ...
