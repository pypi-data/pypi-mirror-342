from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.psdk_interfaces.msg import file_attributes_pb2 as _file_attributes_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SubFileInfo(_message.Message):
    __slots__ = ["header", "name", "type", "size", "index", "create_time_unix", "attributes"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    CREATE_TIME_UNIX_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    name: str
    type: int
    size: int
    index: int
    create_time_unix: int
    attributes: _file_attributes_pb2.FileAttributes
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., name: _Optional[str] = ..., type: _Optional[int] = ..., size: _Optional[int] = ..., index: _Optional[int] = ..., create_time_unix: _Optional[int] = ..., attributes: _Optional[_Union[_file_attributes_pb2.FileAttributes, _Mapping]] = ...) -> None: ...
