from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class COWriteIDRequest(_message.Message):
    __slots__ = ["nodeid", "index", "subindex", "data", "canopen_datatype"]
    NODEID_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    SUBINDEX_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    CANOPEN_DATATYPE_FIELD_NUMBER: _ClassVar[int]
    nodeid: int
    index: int
    subindex: int
    data: int
    canopen_datatype: int
    def __init__(self, nodeid: _Optional[int] = ..., index: _Optional[int] = ..., subindex: _Optional[int] = ..., data: _Optional[int] = ..., canopen_datatype: _Optional[int] = ...) -> None: ...

class COWriteIDResponse(_message.Message):
    __slots__ = ["success"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
