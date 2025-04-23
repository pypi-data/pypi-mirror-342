from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PublishersRequest(_message.Message):
    __slots__ = ["header", "topic"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TOPIC_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    topic: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., topic: _Optional[str] = ...) -> None: ...

class PublishersResponse(_message.Message):
    __slots__ = ["header", "publishers"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PUBLISHERS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    publishers: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., publishers: _Optional[_Iterable[str]] = ...) -> None: ...
