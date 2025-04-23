from make87_messages_ros2.jazzy.std_msgs.msg import multi_array_dimension_pb2 as _multi_array_dimension_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MultiArrayLayout(_message.Message):
    __slots__ = ["dim", "data_offset"]
    DIM_FIELD_NUMBER: _ClassVar[int]
    DATA_OFFSET_FIELD_NUMBER: _ClassVar[int]
    dim: _containers.RepeatedCompositeFieldContainer[_multi_array_dimension_pb2.MultiArrayDimension]
    data_offset: int
    def __init__(self, dim: _Optional[_Iterable[_Union[_multi_array_dimension_pb2.MultiArrayDimension, _Mapping]]] = ..., data_offset: _Optional[int] = ...) -> None: ...
