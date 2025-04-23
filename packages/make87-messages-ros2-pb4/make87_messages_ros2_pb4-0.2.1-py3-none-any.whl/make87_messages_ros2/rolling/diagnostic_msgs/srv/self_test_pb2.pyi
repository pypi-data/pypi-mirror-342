from make87_messages_ros2.rolling.diagnostic_msgs.msg import diagnostic_status_pb2 as _diagnostic_status_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SelfTestRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class SelfTestResponse(_message.Message):
    __slots__ = ["id", "passed", "status"]
    ID_FIELD_NUMBER: _ClassVar[int]
    PASSED_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    id: str
    passed: int
    status: _containers.RepeatedCompositeFieldContainer[_diagnostic_status_pb2.DiagnosticStatus]
    def __init__(self, id: _Optional[str] = ..., passed: _Optional[int] = ..., status: _Optional[_Iterable[_Union[_diagnostic_status_pb2.DiagnosticStatus, _Mapping]]] = ...) -> None: ...
