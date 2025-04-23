from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AdaptiveCruiseControlCommand(_message.Message):
    __slots__ = ["header", "msg_counter", "set_speed", "set", "resume", "cancel", "speed_up", "slow_down", "further", "closer"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MSG_COUNTER_FIELD_NUMBER: _ClassVar[int]
    SET_SPEED_FIELD_NUMBER: _ClassVar[int]
    SET_FIELD_NUMBER: _ClassVar[int]
    RESUME_FIELD_NUMBER: _ClassVar[int]
    CANCEL_FIELD_NUMBER: _ClassVar[int]
    SPEED_UP_FIELD_NUMBER: _ClassVar[int]
    SLOW_DOWN_FIELD_NUMBER: _ClassVar[int]
    FURTHER_FIELD_NUMBER: _ClassVar[int]
    CLOSER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    msg_counter: int
    set_speed: float
    set: int
    resume: int
    cancel: int
    speed_up: int
    slow_down: int
    further: int
    closer: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., msg_counter: _Optional[int] = ..., set_speed: _Optional[float] = ..., set: _Optional[int] = ..., resume: _Optional[int] = ..., cancel: _Optional[int] = ..., speed_up: _Optional[int] = ..., slow_down: _Optional[int] = ..., further: _Optional[int] = ..., closer: _Optional[int] = ...) -> None: ...
