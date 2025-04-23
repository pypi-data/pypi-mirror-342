from make87_messages_ros2.jazzy.mavros_msgs.msg import file_entry_pb2 as _file_entry_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FileListRequest(_message.Message):
    __slots__ = ["dir_path"]
    DIR_PATH_FIELD_NUMBER: _ClassVar[int]
    dir_path: str
    def __init__(self, dir_path: _Optional[str] = ...) -> None: ...

class FileListResponse(_message.Message):
    __slots__ = ["list", "success", "r_errno"]
    LIST_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    R_ERRNO_FIELD_NUMBER: _ClassVar[int]
    list: _containers.RepeatedCompositeFieldContainer[_file_entry_pb2.FileEntry]
    success: bool
    r_errno: int
    def __init__(self, list: _Optional[_Iterable[_Union[_file_entry_pb2.FileEntry, _Mapping]]] = ..., success: bool = ..., r_errno: _Optional[int] = ...) -> None: ...
