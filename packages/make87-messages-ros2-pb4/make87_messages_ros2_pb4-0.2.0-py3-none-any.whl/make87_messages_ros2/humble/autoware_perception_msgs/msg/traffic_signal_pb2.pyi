from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.autoware_perception_msgs.msg import traffic_signal_element_pb2 as _traffic_signal_element_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TrafficSignal(_message.Message):
    __slots__ = ["header", "traffic_signal_id", "elements"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TRAFFIC_SIGNAL_ID_FIELD_NUMBER: _ClassVar[int]
    ELEMENTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    traffic_signal_id: int
    elements: _containers.RepeatedCompositeFieldContainer[_traffic_signal_element_pb2.TrafficSignalElement]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., traffic_signal_id: _Optional[int] = ..., elements: _Optional[_Iterable[_Union[_traffic_signal_element_pb2.TrafficSignalElement, _Mapping]]] = ...) -> None: ...
