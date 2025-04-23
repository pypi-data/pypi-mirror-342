from make87_messages_ros2.jazzy.builtin_interfaces.msg import duration_pb2 as _duration_pb2
from make87_messages_ros2.jazzy.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PlayRequest(_message.Message):
    __slots__ = ["start_offset", "playback_duration", "playback_until_timestamp"]
    START_OFFSET_FIELD_NUMBER: _ClassVar[int]
    PLAYBACK_DURATION_FIELD_NUMBER: _ClassVar[int]
    PLAYBACK_UNTIL_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    start_offset: _time_pb2.Time
    playback_duration: _duration_pb2.Duration
    playback_until_timestamp: _time_pb2.Time
    def __init__(self, start_offset: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., playback_duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., playback_until_timestamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ...) -> None: ...

class PlayResponse(_message.Message):
    __slots__ = ["success"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
