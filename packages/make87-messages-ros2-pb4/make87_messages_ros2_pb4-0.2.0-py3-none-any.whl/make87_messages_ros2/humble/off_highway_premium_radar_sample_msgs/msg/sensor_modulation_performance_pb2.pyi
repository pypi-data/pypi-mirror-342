from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SensorModulationPerformance(_message.Message):
    __slots__ = ["header", "detection_of_measurement_program", "modulation_id", "distance_range_scaling", "separability_distance", "separability_relative_velocity", "precision_distance", "precision_relative_velocity", "covariance_of_distance_and_relative_velocity", "minimum_measurable_distance", "maximum_measurable_distance", "minimum_measurable_relative_velocity", "maximum_measurable_relative_velocity"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DETECTION_OF_MEASUREMENT_PROGRAM_FIELD_NUMBER: _ClassVar[int]
    MODULATION_ID_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_RANGE_SCALING_FIELD_NUMBER: _ClassVar[int]
    SEPARABILITY_DISTANCE_FIELD_NUMBER: _ClassVar[int]
    SEPARABILITY_RELATIVE_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    PRECISION_DISTANCE_FIELD_NUMBER: _ClassVar[int]
    PRECISION_RELATIVE_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    COVARIANCE_OF_DISTANCE_AND_RELATIVE_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    MINIMUM_MEASURABLE_DISTANCE_FIELD_NUMBER: _ClassVar[int]
    MAXIMUM_MEASURABLE_DISTANCE_FIELD_NUMBER: _ClassVar[int]
    MINIMUM_MEASURABLE_RELATIVE_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    MAXIMUM_MEASURABLE_RELATIVE_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    detection_of_measurement_program: int
    modulation_id: int
    distance_range_scaling: float
    separability_distance: float
    separability_relative_velocity: float
    precision_distance: float
    precision_relative_velocity: float
    covariance_of_distance_and_relative_velocity: float
    minimum_measurable_distance: float
    maximum_measurable_distance: float
    minimum_measurable_relative_velocity: float
    maximum_measurable_relative_velocity: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., detection_of_measurement_program: _Optional[int] = ..., modulation_id: _Optional[int] = ..., distance_range_scaling: _Optional[float] = ..., separability_distance: _Optional[float] = ..., separability_relative_velocity: _Optional[float] = ..., precision_distance: _Optional[float] = ..., precision_relative_velocity: _Optional[float] = ..., covariance_of_distance_and_relative_velocity: _Optional[float] = ..., minimum_measurable_distance: _Optional[float] = ..., maximum_measurable_distance: _Optional[float] = ..., minimum_measurable_relative_velocity: _Optional[float] = ..., maximum_measurable_relative_velocity: _Optional[float] = ...) -> None: ...
