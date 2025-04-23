from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from make87_messages_ros2.humble.rmf_task_msgs.msg import task_description_pb2 as _task_description_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TaskProfile(_message.Message):
    __slots__ = ["header", "task_id", "submission_time", "description"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    SUBMISSION_TIME_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    task_id: str
    submission_time: _time_pb2.Time
    description: _task_description_pb2.TaskDescription
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., task_id: _Optional[str] = ..., submission_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., description: _Optional[_Union[_task_description_pb2.TaskDescription, _Mapping]] = ...) -> None: ...
