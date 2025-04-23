from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Start(_message.Message):
    __slots__ = ["header", "recording_frequency", "ignore_nodes", "ignore_topics", "select_nodes", "select_topics"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    RECORDING_FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    IGNORE_NODES_FIELD_NUMBER: _ClassVar[int]
    IGNORE_TOPICS_FIELD_NUMBER: _ClassVar[int]
    SELECT_NODES_FIELD_NUMBER: _ClassVar[int]
    SELECT_TOPICS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    recording_frequency: int
    ignore_nodes: str
    ignore_topics: str
    select_nodes: str
    select_topics: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., recording_frequency: _Optional[int] = ..., ignore_nodes: _Optional[str] = ..., ignore_topics: _Optional[str] = ..., select_nodes: _Optional[str] = ..., select_topics: _Optional[str] = ...) -> None: ...
