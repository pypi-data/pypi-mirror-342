from make87_messages_ros2.jazzy.rmf_fleet_msgs.msg import dock_parameter_pb2 as _dock_parameter_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Dock(_message.Message):
    __slots__ = ["fleet_name", "params"]
    FLEET_NAME_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    fleet_name: str
    params: _containers.RepeatedCompositeFieldContainer[_dock_parameter_pb2.DockParameter]
    def __init__(self, fleet_name: _Optional[str] = ..., params: _Optional[_Iterable[_Union[_dock_parameter_pb2.DockParameter, _Mapping]]] = ...) -> None: ...
