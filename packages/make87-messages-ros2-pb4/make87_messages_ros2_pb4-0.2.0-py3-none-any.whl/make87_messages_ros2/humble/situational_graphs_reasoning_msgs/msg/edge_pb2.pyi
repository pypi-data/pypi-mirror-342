from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import transform_pb2 as _transform_pb2
from make87_messages_ros2.humble.situational_graphs_reasoning_msgs.msg import attribute_pb2 as _attribute_pb2
from make87_messages_ros2.humble.std_msgs.msg import float64_multi_array_pb2 as _float64_multi_array_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Edge(_message.Message):
    __slots__ = ["header", "origin_node", "target_node", "edge_id", "plane_coefficients", "plane_information_matrix", "information_matrix", "measurement_transform", "attributes"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_NODE_FIELD_NUMBER: _ClassVar[int]
    TARGET_NODE_FIELD_NUMBER: _ClassVar[int]
    EDGE_ID_FIELD_NUMBER: _ClassVar[int]
    PLANE_COEFFICIENTS_FIELD_NUMBER: _ClassVar[int]
    PLANE_INFORMATION_MATRIX_FIELD_NUMBER: _ClassVar[int]
    INFORMATION_MATRIX_FIELD_NUMBER: _ClassVar[int]
    MEASUREMENT_TRANSFORM_FIELD_NUMBER: _ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    origin_node: int
    target_node: int
    edge_id: int
    plane_coefficients: _containers.RepeatedScalarFieldContainer[float]
    plane_information_matrix: _containers.RepeatedScalarFieldContainer[float]
    information_matrix: _float64_multi_array_pb2.Float64MultiArray
    measurement_transform: _transform_pb2.Transform
    attributes: _containers.RepeatedCompositeFieldContainer[_attribute_pb2.Attribute]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., origin_node: _Optional[int] = ..., target_node: _Optional[int] = ..., edge_id: _Optional[int] = ..., plane_coefficients: _Optional[_Iterable[float]] = ..., plane_information_matrix: _Optional[_Iterable[float]] = ..., information_matrix: _Optional[_Union[_float64_multi_array_pb2.Float64MultiArray, _Mapping]] = ..., measurement_transform: _Optional[_Union[_transform_pb2.Transform, _Mapping]] = ..., attributes: _Optional[_Iterable[_Union[_attribute_pb2.Attribute, _Mapping]]] = ...) -> None: ...
