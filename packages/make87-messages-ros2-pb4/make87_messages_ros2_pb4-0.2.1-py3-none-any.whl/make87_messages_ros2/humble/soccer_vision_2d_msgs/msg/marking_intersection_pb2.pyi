from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.soccer_vision_attribute_msgs.msg import confidence_pb2 as _confidence_pb2
from make87_messages_ros2.humble.vision_msgs.msg import point2_d_pb2 as _point2_d_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MarkingIntersection(_message.Message):
    __slots__ = ["header", "center", "num_rays", "heading_rays", "confidence"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CENTER_FIELD_NUMBER: _ClassVar[int]
    NUM_RAYS_FIELD_NUMBER: _ClassVar[int]
    HEADING_RAYS_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    center: _point2_d_pb2.Point2D
    num_rays: int
    heading_rays: _containers.RepeatedScalarFieldContainer[float]
    confidence: _confidence_pb2.Confidence
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., center: _Optional[_Union[_point2_d_pb2.Point2D, _Mapping]] = ..., num_rays: _Optional[int] = ..., heading_rays: _Optional[_Iterable[float]] = ..., confidence: _Optional[_Union[_confidence_pb2.Confidence, _Mapping]] = ...) -> None: ...
