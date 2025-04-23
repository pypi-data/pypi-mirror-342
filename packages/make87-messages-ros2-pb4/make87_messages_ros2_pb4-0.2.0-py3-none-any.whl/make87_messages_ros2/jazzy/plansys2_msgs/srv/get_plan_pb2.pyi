from make87_messages_ros2.jazzy.plansys2_msgs.msg import plan_pb2 as _plan_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetPlanRequest(_message.Message):
    __slots__ = ["domain", "problem"]
    DOMAIN_FIELD_NUMBER: _ClassVar[int]
    PROBLEM_FIELD_NUMBER: _ClassVar[int]
    domain: str
    problem: str
    def __init__(self, domain: _Optional[str] = ..., problem: _Optional[str] = ...) -> None: ...

class GetPlanResponse(_message.Message):
    __slots__ = ["success", "plan", "error_info"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    PLAN_FIELD_NUMBER: _ClassVar[int]
    ERROR_INFO_FIELD_NUMBER: _ClassVar[int]
    success: bool
    plan: _plan_pb2.Plan
    error_info: str
    def __init__(self, success: bool = ..., plan: _Optional[_Union[_plan_pb2.Plan, _Mapping]] = ..., error_info: _Optional[str] = ...) -> None: ...
