from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class StreamRateRequest(_message.Message):
    __slots__ = ["stream_id", "message_rate", "on_off"]
    STREAM_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_RATE_FIELD_NUMBER: _ClassVar[int]
    ON_OFF_FIELD_NUMBER: _ClassVar[int]
    stream_id: int
    message_rate: int
    on_off: bool
    def __init__(self, stream_id: _Optional[int] = ..., message_rate: _Optional[int] = ..., on_off: bool = ...) -> None: ...

class StreamRateResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
