from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.actionlib_msgs.msg import goal_id_pb2 as _goal_id_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GoalStatus(_message.Message):
    __slots__ = ["header", "goal_id", "status", "text"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    GOAL_ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    goal_id: _goal_id_pb2.GoalID
    status: int
    text: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., goal_id: _Optional[_Union[_goal_id_pb2.GoalID, _Mapping]] = ..., status: _Optional[int] = ..., text: _Optional[str] = ...) -> None: ...
