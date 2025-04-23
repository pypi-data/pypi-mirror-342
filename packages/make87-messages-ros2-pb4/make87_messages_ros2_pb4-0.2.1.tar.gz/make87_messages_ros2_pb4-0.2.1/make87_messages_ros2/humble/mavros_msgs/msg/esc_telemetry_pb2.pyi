from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.mavros_msgs.msg import esc_telemetry_item_pb2 as _esc_telemetry_item_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ESCTelemetry(_message.Message):
    __slots__ = ["header", "ros2_header", "esc_telemetry"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    ESC_TELEMETRY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    esc_telemetry: _containers.RepeatedCompositeFieldContainer[_esc_telemetry_item_pb2.ESCTelemetryItem]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., esc_telemetry: _Optional[_Iterable[_Union[_esc_telemetry_item_pb2.ESCTelemetryItem, _Mapping]]] = ...) -> None: ...
