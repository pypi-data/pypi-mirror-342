from make87_messages_ros2.rolling.geographic_msgs.msg import geo_point_pb2 as _geo_point_pb2
from make87_messages_ros2.rolling.geometry_msgs.msg import quaternion_pb2 as _quaternion_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CameraImageCaptured(_message.Message):
    __slots__ = ["header", "orientation", "geo", "relative_alt", "image_index", "capture_result", "file_url"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    GEO_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_ALT_FIELD_NUMBER: _ClassVar[int]
    IMAGE_INDEX_FIELD_NUMBER: _ClassVar[int]
    CAPTURE_RESULT_FIELD_NUMBER: _ClassVar[int]
    FILE_URL_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    orientation: _quaternion_pb2.Quaternion
    geo: _geo_point_pb2.GeoPoint
    relative_alt: float
    image_index: int
    capture_result: int
    file_url: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., orientation: _Optional[_Union[_quaternion_pb2.Quaternion, _Mapping]] = ..., geo: _Optional[_Union[_geo_point_pb2.GeoPoint, _Mapping]] = ..., relative_alt: _Optional[float] = ..., image_index: _Optional[int] = ..., capture_result: _Optional[int] = ..., file_url: _Optional[str] = ...) -> None: ...
