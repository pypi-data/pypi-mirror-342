from make87_messages_ros2.rolling.soccer_vision_attribute_msgs.msg import confidence_pb2 as _confidence_pb2
from make87_messages_ros2.rolling.vision_msgs.msg import bounding_box2_d_pb2 as _bounding_box2_d_pb2
from make87_messages_ros2.rolling.vision_msgs.msg import point2_d_pb2 as _point2_d_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Ball(_message.Message):
    __slots__ = ["bb", "center", "confidence"]
    BB_FIELD_NUMBER: _ClassVar[int]
    CENTER_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    bb: _bounding_box2_d_pb2.BoundingBox2D
    center: _point2_d_pb2.Point2D
    confidence: _confidence_pb2.Confidence
    def __init__(self, bb: _Optional[_Union[_bounding_box2_d_pb2.BoundingBox2D, _Mapping]] = ..., center: _Optional[_Union[_point2_d_pb2.Point2D, _Mapping]] = ..., confidence: _Optional[_Union[_confidence_pb2.Confidence, _Mapping]] = ...) -> None: ...
