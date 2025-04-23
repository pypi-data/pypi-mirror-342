from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class TestMultipleRequestFieldsRequest(_message.Message):
    __slots__ = ["int_value", "float_value", "string", "bool_value"]
    INT_VALUE_FIELD_NUMBER: _ClassVar[int]
    FLOAT_VALUE_FIELD_NUMBER: _ClassVar[int]
    STRING_FIELD_NUMBER: _ClassVar[int]
    BOOL_VALUE_FIELD_NUMBER: _ClassVar[int]
    int_value: int
    float_value: float
    string: str
    bool_value: bool
    def __init__(self, int_value: _Optional[int] = ..., float_value: _Optional[float] = ..., string: _Optional[str] = ..., bool_value: bool = ...) -> None: ...

class TestMultipleRequestFieldsResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
