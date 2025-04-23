from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SensorFieldOfView(_message.Message):
    __slots__ = ["header", "fov", "azimuth", "elevation_range_scaling", "elevation"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FOV_FIELD_NUMBER: _ClassVar[int]
    AZIMUTH_FIELD_NUMBER: _ClassVar[int]
    ELEVATION_RANGE_SCALING_FIELD_NUMBER: _ClassVar[int]
    ELEVATION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    fov: _containers.RepeatedScalarFieldContainer[float]
    azimuth: _containers.RepeatedScalarFieldContainer[float]
    elevation_range_scaling: _containers.RepeatedScalarFieldContainer[float]
    elevation: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., fov: _Optional[_Iterable[float]] = ..., azimuth: _Optional[_Iterable[float]] = ..., elevation_range_scaling: _Optional[_Iterable[float]] = ..., elevation: _Optional[_Iterable[float]] = ...) -> None: ...
