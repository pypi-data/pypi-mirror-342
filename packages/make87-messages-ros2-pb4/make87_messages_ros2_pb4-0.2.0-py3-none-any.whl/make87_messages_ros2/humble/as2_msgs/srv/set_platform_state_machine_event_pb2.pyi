from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.as2_msgs.msg import platform_state_machine_event_pb2 as _platform_state_machine_event_pb2
from make87_messages_ros2.humble.as2_msgs.msg import platform_status_pb2 as _platform_status_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetPlatformStateMachineEventRequest(_message.Message):
    __slots__ = ["header", "event"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    EVENT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    event: _platform_state_machine_event_pb2.PlatformStateMachineEvent
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., event: _Optional[_Union[_platform_state_machine_event_pb2.PlatformStateMachineEvent, _Mapping]] = ...) -> None: ...

class SetPlatformStateMachineEventResponse(_message.Message):
    __slots__ = ["header", "success", "current_state"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    CURRENT_STATE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    current_state: _platform_status_pb2.PlatformStatus
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., current_state: _Optional[_Union[_platform_status_pb2.PlatformStatus, _Mapping]] = ...) -> None: ...
