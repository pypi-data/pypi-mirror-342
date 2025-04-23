from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import point_pb2 as _point_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from make87_messages_ros2.humble.soccer_vision_attribute_msgs.msg import confidence_pb2 as _confidence_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MarkingIntersection(_message.Message):
    __slots__ = ["header", "center", "num_rays", "rays", "confidence"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CENTER_FIELD_NUMBER: _ClassVar[int]
    NUM_RAYS_FIELD_NUMBER: _ClassVar[int]
    RAYS_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    center: _point_pb2.Point
    num_rays: int
    rays: _containers.RepeatedCompositeFieldContainer[_vector3_pb2.Vector3]
    confidence: _confidence_pb2.Confidence
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., center: _Optional[_Union[_point_pb2.Point, _Mapping]] = ..., num_rays: _Optional[int] = ..., rays: _Optional[_Iterable[_Union[_vector3_pb2.Vector3, _Mapping]]] = ..., confidence: _Optional[_Union[_confidence_pb2.Confidence, _Mapping]] = ...) -> None: ...
