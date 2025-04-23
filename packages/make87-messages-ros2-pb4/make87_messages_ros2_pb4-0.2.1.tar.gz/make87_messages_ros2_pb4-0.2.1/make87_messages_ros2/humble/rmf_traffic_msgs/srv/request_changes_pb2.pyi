from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rmf_traffic_msgs.msg import schedule_identity_pb2 as _schedule_identity_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RequestChangesRequest(_message.Message):
    __slots__ = ["header", "query_id", "version", "full_update"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    FULL_UPDATE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    query_id: int
    version: int
    full_update: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., query_id: _Optional[int] = ..., version: _Optional[int] = ..., full_update: bool = ...) -> None: ...

class RequestChangesResponse(_message.Message):
    __slots__ = ["header", "node_id", "result", "error"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    node_id: _schedule_identity_pb2.ScheduleIdentity
    result: int
    error: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., node_id: _Optional[_Union[_schedule_identity_pb2.ScheduleIdentity, _Mapping]] = ..., result: _Optional[int] = ..., error: _Optional[str] = ...) -> None: ...
