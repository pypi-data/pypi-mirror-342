from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CameraShootIntervalPhotoRequest(_message.Message):
    __slots__ = ["header", "payload_index", "num_photos_to_capture", "time_interval"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_INDEX_FIELD_NUMBER: _ClassVar[int]
    NUM_PHOTOS_TO_CAPTURE_FIELD_NUMBER: _ClassVar[int]
    TIME_INTERVAL_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    payload_index: int
    num_photos_to_capture: int
    time_interval: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., payload_index: _Optional[int] = ..., num_photos_to_capture: _Optional[int] = ..., time_interval: _Optional[int] = ...) -> None: ...

class CameraShootIntervalPhotoResponse(_message.Message):
    __slots__ = ["header", "success"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ...) -> None: ...
