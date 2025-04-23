from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ApiRequest(_message.Message):
    __slots__ = ["header", "json_msg", "request_id"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    JSON_MSG_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    json_msg: str
    request_id: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., json_msg: _Optional[str] = ..., request_id: _Optional[str] = ...) -> None: ...
