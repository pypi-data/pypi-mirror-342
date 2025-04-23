from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LiftClearanceRequest(_message.Message):
    __slots__ = ["header", "robot_name", "lift_name"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROBOT_NAME_FIELD_NUMBER: _ClassVar[int]
    LIFT_NAME_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    robot_name: str
    lift_name: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., robot_name: _Optional[str] = ..., lift_name: _Optional[str] = ...) -> None: ...

class LiftClearanceResponse(_message.Message):
    __slots__ = ["header", "decision"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DECISION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    decision: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., decision: _Optional[int] = ...) -> None: ...
