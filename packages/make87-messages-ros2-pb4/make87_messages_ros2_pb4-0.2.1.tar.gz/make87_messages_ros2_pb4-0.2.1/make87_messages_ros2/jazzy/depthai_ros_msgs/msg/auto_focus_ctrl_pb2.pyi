from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AutoFocusCtrl(_message.Message):
    __slots__ = ["auto_focus_mode", "trigger_auto_focus"]
    AUTO_FOCUS_MODE_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_AUTO_FOCUS_FIELD_NUMBER: _ClassVar[int]
    auto_focus_mode: int
    trigger_auto_focus: bool
    def __init__(self, auto_focus_mode: _Optional[int] = ..., trigger_auto_focus: bool = ...) -> None: ...
