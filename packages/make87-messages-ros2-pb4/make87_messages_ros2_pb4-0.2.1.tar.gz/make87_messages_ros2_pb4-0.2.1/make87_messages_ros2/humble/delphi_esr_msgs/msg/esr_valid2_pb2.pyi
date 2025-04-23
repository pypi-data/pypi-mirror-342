from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EsrValid2(_message.Message):
    __slots__ = ["header", "ros2_header", "canmsg", "mr_sn", "mr_range", "mr_range_rate", "mr_angle", "mr_power"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    CANMSG_FIELD_NUMBER: _ClassVar[int]
    MR_SN_FIELD_NUMBER: _ClassVar[int]
    MR_RANGE_FIELD_NUMBER: _ClassVar[int]
    MR_RANGE_RATE_FIELD_NUMBER: _ClassVar[int]
    MR_ANGLE_FIELD_NUMBER: _ClassVar[int]
    MR_POWER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    canmsg: str
    mr_sn: int
    mr_range: float
    mr_range_rate: float
    mr_angle: float
    mr_power: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., canmsg: _Optional[str] = ..., mr_sn: _Optional[int] = ..., mr_range: _Optional[float] = ..., mr_range_rate: _Optional[float] = ..., mr_angle: _Optional[float] = ..., mr_power: _Optional[int] = ...) -> None: ...
