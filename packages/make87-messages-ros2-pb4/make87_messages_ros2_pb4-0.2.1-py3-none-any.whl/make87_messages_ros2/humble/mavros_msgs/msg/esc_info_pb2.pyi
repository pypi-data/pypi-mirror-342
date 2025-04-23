from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.mavros_msgs.msg import esc_info_item_pb2 as _esc_info_item_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ESCInfo(_message.Message):
    __slots__ = ["header", "ros2_header", "counter", "count", "connection_type", "info", "esc_info"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    COUNTER_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    INFO_FIELD_NUMBER: _ClassVar[int]
    ESC_INFO_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    counter: int
    count: int
    connection_type: int
    info: int
    esc_info: _containers.RepeatedCompositeFieldContainer[_esc_info_item_pb2.ESCInfoItem]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., counter: _Optional[int] = ..., count: _Optional[int] = ..., connection_type: _Optional[int] = ..., info: _Optional[int] = ..., esc_info: _Optional[_Iterable[_Union[_esc_info_item_pb2.ESCInfoItem, _Mapping]]] = ...) -> None: ...
