from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RenameRobotStateInWarehouseRequest(_message.Message):
    __slots__ = ["old_name", "new_name", "robot"]
    OLD_NAME_FIELD_NUMBER: _ClassVar[int]
    NEW_NAME_FIELD_NUMBER: _ClassVar[int]
    ROBOT_FIELD_NUMBER: _ClassVar[int]
    old_name: str
    new_name: str
    robot: str
    def __init__(self, old_name: _Optional[str] = ..., new_name: _Optional[str] = ..., robot: _Optional[str] = ...) -> None: ...

class RenameRobotStateInWarehouseResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
