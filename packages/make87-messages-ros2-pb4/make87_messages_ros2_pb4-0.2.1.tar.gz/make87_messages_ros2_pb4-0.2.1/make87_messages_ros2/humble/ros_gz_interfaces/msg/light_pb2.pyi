from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from make87_messages_ros2.humble.std_msgs.msg import color_rgba_pb2 as _color_rgba_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Light(_message.Message):
    __slots__ = ["header", "ros2_header", "name", "type", "pose", "diffuse", "specular", "attenuation_constant", "attenuation_linear", "attenuation_quadratic", "direction", "range", "cast_shadows", "spot_inner_angle", "spot_outer_angle", "spot_falloff", "id", "parent_id", "intensity"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    DIFFUSE_FIELD_NUMBER: _ClassVar[int]
    SPECULAR_FIELD_NUMBER: _ClassVar[int]
    ATTENUATION_CONSTANT_FIELD_NUMBER: _ClassVar[int]
    ATTENUATION_LINEAR_FIELD_NUMBER: _ClassVar[int]
    ATTENUATION_QUADRATIC_FIELD_NUMBER: _ClassVar[int]
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    RANGE_FIELD_NUMBER: _ClassVar[int]
    CAST_SHADOWS_FIELD_NUMBER: _ClassVar[int]
    SPOT_INNER_ANGLE_FIELD_NUMBER: _ClassVar[int]
    SPOT_OUTER_ANGLE_FIELD_NUMBER: _ClassVar[int]
    SPOT_FALLOFF_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    PARENT_ID_FIELD_NUMBER: _ClassVar[int]
    INTENSITY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    name: str
    type: int
    pose: _pose_pb2.Pose
    diffuse: _color_rgba_pb2.ColorRGBA
    specular: _color_rgba_pb2.ColorRGBA
    attenuation_constant: float
    attenuation_linear: float
    attenuation_quadratic: float
    direction: _vector3_pb2.Vector3
    range: float
    cast_shadows: bool
    spot_inner_angle: float
    spot_outer_angle: float
    spot_falloff: float
    id: int
    parent_id: int
    intensity: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., name: _Optional[str] = ..., type: _Optional[int] = ..., pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., diffuse: _Optional[_Union[_color_rgba_pb2.ColorRGBA, _Mapping]] = ..., specular: _Optional[_Union[_color_rgba_pb2.ColorRGBA, _Mapping]] = ..., attenuation_constant: _Optional[float] = ..., attenuation_linear: _Optional[float] = ..., attenuation_quadratic: _Optional[float] = ..., direction: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., range: _Optional[float] = ..., cast_shadows: bool = ..., spot_inner_angle: _Optional[float] = ..., spot_outer_angle: _Optional[float] = ..., spot_falloff: _Optional[float] = ..., id: _Optional[int] = ..., parent_id: _Optional[int] = ..., intensity: _Optional[float] = ...) -> None: ...
