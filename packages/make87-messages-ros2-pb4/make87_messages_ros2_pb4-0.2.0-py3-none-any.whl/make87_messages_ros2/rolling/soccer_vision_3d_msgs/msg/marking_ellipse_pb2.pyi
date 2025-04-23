from make87_messages_ros2.rolling.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.rolling.soccer_vision_attribute_msgs.msg import confidence_pb2 as _confidence_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MarkingEllipse(_message.Message):
    __slots__ = ["diameter", "center", "confidence"]
    DIAMETER_FIELD_NUMBER: _ClassVar[int]
    CENTER_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    diameter: float
    center: _pose_pb2.Pose
    confidence: _confidence_pb2.Confidence
    def __init__(self, diameter: _Optional[float] = ..., center: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., confidence: _Optional[_Union[_confidence_pb2.Confidence, _Mapping]] = ...) -> None: ...
