from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from make87_messages_ros2.rolling.tuw_multi_robot_msgs.msg import order_pb2 as _order_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class OrderArray(_message.Message):
    __slots__ = ["header", "orders"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ORDERS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    orders: _containers.RepeatedCompositeFieldContainer[_order_pb2.Order]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., orders: _Optional[_Iterable[_Union[_order_pb2.Order, _Mapping]]] = ...) -> None: ...
