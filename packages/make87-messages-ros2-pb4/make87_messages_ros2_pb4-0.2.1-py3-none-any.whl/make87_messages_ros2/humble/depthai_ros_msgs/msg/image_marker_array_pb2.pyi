from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.visualization_msgs.msg import image_marker_pb2 as _image_marker_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ImageMarkerArray(_message.Message):
    __slots__ = ["header", "markers"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MARKERS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    markers: _containers.RepeatedCompositeFieldContainer[_image_marker_pb2.ImageMarker]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., markers: _Optional[_Iterable[_Union[_image_marker_pb2.ImageMarker, _Mapping]]] = ...) -> None: ...
