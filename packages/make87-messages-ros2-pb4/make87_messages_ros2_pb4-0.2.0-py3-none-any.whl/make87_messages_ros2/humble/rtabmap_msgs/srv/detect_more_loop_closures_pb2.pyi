from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DetectMoreLoopClosuresRequest(_message.Message):
    __slots__ = ["header", "cluster_radius_max", "cluster_radius_min", "cluster_angle", "iterations", "intra_only", "inter_only"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_RADIUS_MAX_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_RADIUS_MIN_FIELD_NUMBER: _ClassVar[int]
    CLUSTER_ANGLE_FIELD_NUMBER: _ClassVar[int]
    ITERATIONS_FIELD_NUMBER: _ClassVar[int]
    INTRA_ONLY_FIELD_NUMBER: _ClassVar[int]
    INTER_ONLY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    cluster_radius_max: float
    cluster_radius_min: float
    cluster_angle: float
    iterations: int
    intra_only: bool
    inter_only: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., cluster_radius_max: _Optional[float] = ..., cluster_radius_min: _Optional[float] = ..., cluster_angle: _Optional[float] = ..., iterations: _Optional[int] = ..., intra_only: bool = ..., inter_only: bool = ...) -> None: ...

class DetectMoreLoopClosuresResponse(_message.Message):
    __slots__ = ["header", "detected"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DETECTED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    detected: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., detected: _Optional[int] = ...) -> None: ...
