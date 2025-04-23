from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Pickup(_message.Message):
    __slots__ = ["header", "robot_name", "order_id"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROBOT_NAME_FIELD_NUMBER: _ClassVar[int]
    ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    robot_name: str
    order_id: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., robot_name: _Optional[str] = ..., order_id: _Optional[int] = ...) -> None: ...
