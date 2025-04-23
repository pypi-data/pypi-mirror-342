from make87_messages_ros2.jazzy.plansys2_msgs.msg import node_pb2 as _node_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ExistNodeRequest(_message.Message):
    __slots__ = ["node"]
    NODE_FIELD_NUMBER: _ClassVar[int]
    node: _node_pb2.Node
    def __init__(self, node: _Optional[_Union[_node_pb2.Node, _Mapping]] = ...) -> None: ...

class ExistNodeResponse(_message.Message):
    __slots__ = ["exist"]
    EXIST_FIELD_NUMBER: _ClassVar[int]
    exist: bool
    def __init__(self, exist: bool = ...) -> None: ...
