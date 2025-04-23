from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.moveit_msgs.msg import planner_params_pb2 as _planner_params_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetPlannerParamsRequest(_message.Message):
    __slots__ = ["header", "pipeline_id", "planner_config", "group", "params", "replace"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PIPELINE_ID_FIELD_NUMBER: _ClassVar[int]
    PLANNER_CONFIG_FIELD_NUMBER: _ClassVar[int]
    GROUP_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    REPLACE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    pipeline_id: str
    planner_config: str
    group: str
    params: _planner_params_pb2.PlannerParams
    replace: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., pipeline_id: _Optional[str] = ..., planner_config: _Optional[str] = ..., group: _Optional[str] = ..., params: _Optional[_Union[_planner_params_pb2.PlannerParams, _Mapping]] = ..., replace: bool = ...) -> None: ...

class SetPlannerParamsResponse(_message.Message):
    __slots__ = ["header"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...
