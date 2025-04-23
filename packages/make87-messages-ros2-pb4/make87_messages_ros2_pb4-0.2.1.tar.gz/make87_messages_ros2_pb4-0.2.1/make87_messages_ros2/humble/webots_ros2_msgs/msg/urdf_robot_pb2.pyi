from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UrdfRobot(_message.Message):
    __slots__ = ["header", "name", "urdf_path", "robot_description", "relative_path_prefix", "translation", "rotation", "normal", "box_collision", "init_pos"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    URDF_PATH_FIELD_NUMBER: _ClassVar[int]
    ROBOT_DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_PATH_PREFIX_FIELD_NUMBER: _ClassVar[int]
    TRANSLATION_FIELD_NUMBER: _ClassVar[int]
    ROTATION_FIELD_NUMBER: _ClassVar[int]
    NORMAL_FIELD_NUMBER: _ClassVar[int]
    BOX_COLLISION_FIELD_NUMBER: _ClassVar[int]
    INIT_POS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    name: str
    urdf_path: str
    robot_description: str
    relative_path_prefix: str
    translation: str
    rotation: str
    normal: bool
    box_collision: bool
    init_pos: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., name: _Optional[str] = ..., urdf_path: _Optional[str] = ..., robot_description: _Optional[str] = ..., relative_path_prefix: _Optional[str] = ..., translation: _Optional[str] = ..., rotation: _Optional[str] = ..., normal: bool = ..., box_collision: bool = ..., init_pos: _Optional[str] = ...) -> None: ...
