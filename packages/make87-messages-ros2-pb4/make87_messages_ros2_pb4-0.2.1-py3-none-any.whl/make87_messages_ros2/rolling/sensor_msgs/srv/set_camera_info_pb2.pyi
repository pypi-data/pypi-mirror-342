from make87_messages_ros2.rolling.sensor_msgs.msg import camera_info_pb2 as _camera_info_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetCameraInfoRequest(_message.Message):
    __slots__ = ["camera_info"]
    CAMERA_INFO_FIELD_NUMBER: _ClassVar[int]
    camera_info: _camera_info_pb2.CameraInfo
    def __init__(self, camera_info: _Optional[_Union[_camera_info_pb2.CameraInfo, _Mapping]] = ...) -> None: ...

class SetCameraInfoResponse(_message.Message):
    __slots__ = ["success", "status_message"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    status_message: str
    def __init__(self, success: bool = ..., status_message: _Optional[str] = ...) -> None: ...
