from make87_messages_ros2.rolling.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AutowareState(_message.Message):
    __slots__ = ["stamp", "state"]
    STAMP_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    stamp: _time_pb2.Time
    state: int
    def __init__(self, stamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., state: _Optional[int] = ...) -> None: ...
