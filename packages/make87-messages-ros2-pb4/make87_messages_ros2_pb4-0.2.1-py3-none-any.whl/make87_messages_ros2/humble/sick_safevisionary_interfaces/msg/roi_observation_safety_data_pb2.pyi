from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ROIObservationSafetyData(_message.Message):
    __slots__ = ["header", "invalid_due_to_invalid_pixels", "invalid_due_to_variance", "invalid_due_to_overexposure", "invalid_due_to_underexposure", "invalid_due_to_temporal_variance", "invalid_due_to_outside_of_measurement_range", "invalid_due_to_retro_reflector_interference", "contamination_error", "quality_class", "slot_active"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    INVALID_DUE_TO_INVALID_PIXELS_FIELD_NUMBER: _ClassVar[int]
    INVALID_DUE_TO_VARIANCE_FIELD_NUMBER: _ClassVar[int]
    INVALID_DUE_TO_OVEREXPOSURE_FIELD_NUMBER: _ClassVar[int]
    INVALID_DUE_TO_UNDEREXPOSURE_FIELD_NUMBER: _ClassVar[int]
    INVALID_DUE_TO_TEMPORAL_VARIANCE_FIELD_NUMBER: _ClassVar[int]
    INVALID_DUE_TO_OUTSIDE_OF_MEASUREMENT_RANGE_FIELD_NUMBER: _ClassVar[int]
    INVALID_DUE_TO_RETRO_REFLECTOR_INTERFERENCE_FIELD_NUMBER: _ClassVar[int]
    CONTAMINATION_ERROR_FIELD_NUMBER: _ClassVar[int]
    QUALITY_CLASS_FIELD_NUMBER: _ClassVar[int]
    SLOT_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    invalid_due_to_invalid_pixels: int
    invalid_due_to_variance: int
    invalid_due_to_overexposure: int
    invalid_due_to_underexposure: int
    invalid_due_to_temporal_variance: int
    invalid_due_to_outside_of_measurement_range: int
    invalid_due_to_retro_reflector_interference: int
    contamination_error: int
    quality_class: int
    slot_active: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., invalid_due_to_invalid_pixels: _Optional[int] = ..., invalid_due_to_variance: _Optional[int] = ..., invalid_due_to_overexposure: _Optional[int] = ..., invalid_due_to_underexposure: _Optional[int] = ..., invalid_due_to_temporal_variance: _Optional[int] = ..., invalid_due_to_outside_of_measurement_range: _Optional[int] = ..., invalid_due_to_retro_reflector_interference: _Optional[int] = ..., contamination_error: _Optional[int] = ..., quality_class: _Optional[int] = ..., slot_active: _Optional[int] = ...) -> None: ...
