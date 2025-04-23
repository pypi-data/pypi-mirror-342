from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CleanupLocalGridsRequest(_message.Message):
    __slots__ = ["radius", "filter_scans"]
    RADIUS_FIELD_NUMBER: _ClassVar[int]
    FILTER_SCANS_FIELD_NUMBER: _ClassVar[int]
    radius: int
    filter_scans: bool
    def __init__(self, radius: _Optional[int] = ..., filter_scans: bool = ...) -> None: ...

class CleanupLocalGridsResponse(_message.Message):
    __slots__ = ["modified"]
    MODIFIED_FIELD_NUMBER: _ClassVar[int]
    modified: int
    def __init__(self, modified: _Optional[int] = ...) -> None: ...
