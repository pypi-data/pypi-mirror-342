from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.autoware_control_msgs.msg import control_pb2 as _control_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ControlHorizon(_message.Message):
    __slots__ = ["header", "stamp", "control_time", "time_step_ms", "controls"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    STAMP_FIELD_NUMBER: _ClassVar[int]
    CONTROL_TIME_FIELD_NUMBER: _ClassVar[int]
    TIME_STEP_MS_FIELD_NUMBER: _ClassVar[int]
    CONTROLS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    stamp: _time_pb2.Time
    control_time: _time_pb2.Time
    time_step_ms: float
    controls: _containers.RepeatedCompositeFieldContainer[_control_pb2.Control]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., stamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., control_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., time_step_ms: _Optional[float] = ..., controls: _Optional[_Iterable[_Union[_control_pb2.Control, _Mapping]]] = ...) -> None: ...
