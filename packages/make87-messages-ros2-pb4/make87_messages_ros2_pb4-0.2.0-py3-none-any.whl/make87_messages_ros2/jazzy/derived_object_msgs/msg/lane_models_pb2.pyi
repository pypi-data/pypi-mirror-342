from make87_messages_ros2.jazzy.derived_object_msgs.msg import lane_pb2 as _lane_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LaneModels(_message.Message):
    __slots__ = ["header", "left_lane", "right_lane", "additional_lanes"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    LEFT_LANE_FIELD_NUMBER: _ClassVar[int]
    RIGHT_LANE_FIELD_NUMBER: _ClassVar[int]
    ADDITIONAL_LANES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    left_lane: _lane_pb2.Lane
    right_lane: _lane_pb2.Lane
    additional_lanes: _containers.RepeatedCompositeFieldContainer[_lane_pb2.Lane]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., left_lane: _Optional[_Union[_lane_pb2.Lane, _Mapping]] = ..., right_lane: _Optional[_Union[_lane_pb2.Lane, _Mapping]] = ..., additional_lanes: _Optional[_Iterable[_Union[_lane_pb2.Lane, _Mapping]]] = ...) -> None: ...
