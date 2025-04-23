from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Tunnel(_message.Message):
    __slots__ = ["header", "target_system", "target_component", "payload_type", "payload_length", "payload"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TARGET_SYSTEM_FIELD_NUMBER: _ClassVar[int]
    TARGET_COMPONENT_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_TYPE_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_LENGTH_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    target_system: int
    target_component: int
    payload_type: int
    payload_length: int
    payload: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., target_system: _Optional[int] = ..., target_component: _Optional[int] = ..., payload_type: _Optional[int] = ..., payload_length: _Optional[int] = ..., payload: _Optional[_Iterable[int]] = ...) -> None: ...
