from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.soccer_vision_attribute_msgs.msg import confidence_pb2 as _confidence_pb2
from make87_messages_ros2.humble.vision_msgs.msg import point2_d_pb2 as _point2_d_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MarkingSegment(_message.Message):
    __slots__ = ["header", "start", "end", "confidence"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    start: _point2_d_pb2.Point2D
    end: _point2_d_pb2.Point2D
    confidence: _confidence_pb2.Confidence
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., start: _Optional[_Union[_point2_d_pb2.Point2D, _Mapping]] = ..., end: _Optional[_Union[_point2_d_pb2.Point2D, _Mapping]] = ..., confidence: _Optional[_Union[_confidence_pb2.Confidence, _Mapping]] = ...) -> None: ...
