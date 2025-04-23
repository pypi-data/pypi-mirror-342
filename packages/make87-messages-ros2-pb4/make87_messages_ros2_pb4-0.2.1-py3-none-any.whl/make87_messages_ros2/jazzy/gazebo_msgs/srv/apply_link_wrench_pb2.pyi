from make87_messages_ros2.jazzy.builtin_interfaces.msg import duration_pb2 as _duration_pb2
from make87_messages_ros2.jazzy.builtin_interfaces.msg import time_pb2 as _time_pb2
from make87_messages_ros2.jazzy.geometry_msgs.msg import point_pb2 as _point_pb2
from make87_messages_ros2.jazzy.geometry_msgs.msg import wrench_pb2 as _wrench_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ApplyLinkWrenchRequest(_message.Message):
    __slots__ = ["link_name", "reference_frame", "reference_point", "wrench", "start_time", "duration"]
    LINK_NAME_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_FRAME_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_POINT_FIELD_NUMBER: _ClassVar[int]
    WRENCH_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    link_name: str
    reference_frame: str
    reference_point: _point_pb2.Point
    wrench: _wrench_pb2.Wrench
    start_time: _time_pb2.Time
    duration: _duration_pb2.Duration
    def __init__(self, link_name: _Optional[str] = ..., reference_frame: _Optional[str] = ..., reference_point: _Optional[_Union[_point_pb2.Point, _Mapping]] = ..., wrench: _Optional[_Union[_wrench_pb2.Wrench, _Mapping]] = ..., start_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...) -> None: ...

class ApplyLinkWrenchResponse(_message.Message):
    __slots__ = ["success", "status_message"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    status_message: str
    def __init__(self, success: bool = ..., status_message: _Optional[str] = ...) -> None: ...
