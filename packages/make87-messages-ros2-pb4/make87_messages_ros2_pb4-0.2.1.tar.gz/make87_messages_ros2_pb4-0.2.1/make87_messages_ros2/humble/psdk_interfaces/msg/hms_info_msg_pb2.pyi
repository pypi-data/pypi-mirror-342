from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class HmsInfoMsg(_message.Message):
    __slots__ = ["header", "error_code", "component_index", "error_level", "ground_info", "fly_info"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    COMPONENT_INDEX_FIELD_NUMBER: _ClassVar[int]
    ERROR_LEVEL_FIELD_NUMBER: _ClassVar[int]
    GROUND_INFO_FIELD_NUMBER: _ClassVar[int]
    FLY_INFO_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    error_code: int
    component_index: int
    error_level: int
    ground_info: str
    fly_info: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., error_code: _Optional[int] = ..., component_index: _Optional[int] = ..., error_level: _Optional[int] = ..., ground_info: _Optional[str] = ..., fly_info: _Optional[str] = ...) -> None: ...
