from make87_messages_ros2.jazzy.geometry_msgs.msg import transform_pb2 as _transform_pb2
from make87_messages_ros2.jazzy.sensor_msgs.msg import camera_info_pb2 as _camera_info_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CameraModel(_message.Message):
    __slots__ = ["camera_info", "local_transform"]
    CAMERA_INFO_FIELD_NUMBER: _ClassVar[int]
    LOCAL_TRANSFORM_FIELD_NUMBER: _ClassVar[int]
    camera_info: _camera_info_pb2.CameraInfo
    local_transform: _transform_pb2.Transform
    def __init__(self, camera_info: _Optional[_Union[_camera_info_pb2.CameraInfo, _Mapping]] = ..., local_transform: _Optional[_Union[_transform_pb2.Transform, _Mapping]] = ...) -> None: ...
