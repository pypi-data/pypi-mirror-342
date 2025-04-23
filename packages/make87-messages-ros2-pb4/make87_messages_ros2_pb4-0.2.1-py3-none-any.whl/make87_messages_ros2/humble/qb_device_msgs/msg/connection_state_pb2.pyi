from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.qb_device_msgs.msg import device_connection_info_pb2 as _device_connection_info_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ConnectionState(_message.Message):
    __slots__ = ["header", "devices"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DEVICES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    devices: _containers.RepeatedCompositeFieldContainer[_device_connection_info_pb2.DeviceConnectionInfo]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., devices: _Optional[_Iterable[_Union[_device_connection_info_pb2.DeviceConnectionInfo, _Mapping]]] = ...) -> None: ...
