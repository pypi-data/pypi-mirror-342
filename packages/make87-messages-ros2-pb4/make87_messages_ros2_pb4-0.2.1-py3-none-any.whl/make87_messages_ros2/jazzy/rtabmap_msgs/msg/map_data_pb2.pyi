from make87_messages_ros2.jazzy.rtabmap_msgs.msg import map_graph_pb2 as _map_graph_pb2
from make87_messages_ros2.jazzy.rtabmap_msgs.msg import node_pb2 as _node_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MapData(_message.Message):
    __slots__ = ["header", "graph", "nodes"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    GRAPH_FIELD_NUMBER: _ClassVar[int]
    NODES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    graph: _map_graph_pb2.MapGraph
    nodes: _containers.RepeatedCompositeFieldContainer[_node_pb2.Node]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., graph: _Optional[_Union[_map_graph_pb2.MapGraph, _Mapping]] = ..., nodes: _Optional[_Iterable[_Union[_node_pb2.Node, _Mapping]]] = ...) -> None: ...
