from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.hri_actions_msgs.msg import activity_list_pb2 as _activity_list_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ListActivitiesRequest(_message.Message):
    __slots__ = ["header"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...

class ListActivitiesResponse(_message.Message):
    __slots__ = ["header", "activities"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ACTIVITIES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    activities: _activity_list_pb2.ActivityList
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., activities: _Optional[_Union[_activity_list_pb2.ActivityList, _Mapping]] = ...) -> None: ...
