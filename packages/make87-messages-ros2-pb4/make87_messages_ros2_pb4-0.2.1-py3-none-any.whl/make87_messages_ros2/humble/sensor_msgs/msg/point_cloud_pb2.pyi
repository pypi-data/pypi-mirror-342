from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import point32_pb2 as _point32_pb2
from make87_messages_ros2.humble.sensor_msgs.msg import channel_float32_pb2 as _channel_float32_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PointCloud(_message.Message):
    __slots__ = ["header", "ros2_header", "points", "channels"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    CHANNELS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    points: _containers.RepeatedCompositeFieldContainer[_point32_pb2.Point32]
    channels: _containers.RepeatedCompositeFieldContainer[_channel_float32_pb2.ChannelFloat32]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., points: _Optional[_Iterable[_Union[_point32_pb2.Point32, _Mapping]]] = ..., channels: _Optional[_Iterable[_Union[_channel_float32_pb2.ChannelFloat32, _Mapping]]] = ...) -> None: ...
