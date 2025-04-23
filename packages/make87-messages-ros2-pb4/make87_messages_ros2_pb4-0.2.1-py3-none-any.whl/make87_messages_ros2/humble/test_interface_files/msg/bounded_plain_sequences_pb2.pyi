from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.test_interface_files.msg import basic_types_pb2 as _basic_types_pb2
from make87_messages_ros2.humble.test_interface_files.msg import constants_pb2 as _constants_pb2
from make87_messages_ros2.humble.test_interface_files.msg import defaults_pb2 as _defaults_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BoundedPlainSequences(_message.Message):
    __slots__ = ["header", "bool_values", "byte_values", "char_values", "float32_values", "float64_values", "int8_values", "uint8_values", "int16_values", "uint16_values", "int32_values", "uint32_values", "int64_values", "uint64_values", "basic_types_values", "constants_values", "defaults_values", "bool_values_default", "byte_values_default", "char_values_default", "float32_values_default", "float64_values_default", "int8_values_default", "uint8_values_default", "int16_values_default", "uint16_values_default", "int32_values_default", "uint32_values_default", "int64_values_default", "uint64_values_default", "alignment_check"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BOOL_VALUES_FIELD_NUMBER: _ClassVar[int]
    BYTE_VALUES_FIELD_NUMBER: _ClassVar[int]
    CHAR_VALUES_FIELD_NUMBER: _ClassVar[int]
    FLOAT32_VALUES_FIELD_NUMBER: _ClassVar[int]
    FLOAT64_VALUES_FIELD_NUMBER: _ClassVar[int]
    INT8_VALUES_FIELD_NUMBER: _ClassVar[int]
    UINT8_VALUES_FIELD_NUMBER: _ClassVar[int]
    INT16_VALUES_FIELD_NUMBER: _ClassVar[int]
    UINT16_VALUES_FIELD_NUMBER: _ClassVar[int]
    INT32_VALUES_FIELD_NUMBER: _ClassVar[int]
    UINT32_VALUES_FIELD_NUMBER: _ClassVar[int]
    INT64_VALUES_FIELD_NUMBER: _ClassVar[int]
    UINT64_VALUES_FIELD_NUMBER: _ClassVar[int]
    BASIC_TYPES_VALUES_FIELD_NUMBER: _ClassVar[int]
    CONSTANTS_VALUES_FIELD_NUMBER: _ClassVar[int]
    DEFAULTS_VALUES_FIELD_NUMBER: _ClassVar[int]
    BOOL_VALUES_DEFAULT_FIELD_NUMBER: _ClassVar[int]
    BYTE_VALUES_DEFAULT_FIELD_NUMBER: _ClassVar[int]
    CHAR_VALUES_DEFAULT_FIELD_NUMBER: _ClassVar[int]
    FLOAT32_VALUES_DEFAULT_FIELD_NUMBER: _ClassVar[int]
    FLOAT64_VALUES_DEFAULT_FIELD_NUMBER: _ClassVar[int]
    INT8_VALUES_DEFAULT_FIELD_NUMBER: _ClassVar[int]
    UINT8_VALUES_DEFAULT_FIELD_NUMBER: _ClassVar[int]
    INT16_VALUES_DEFAULT_FIELD_NUMBER: _ClassVar[int]
    UINT16_VALUES_DEFAULT_FIELD_NUMBER: _ClassVar[int]
    INT32_VALUES_DEFAULT_FIELD_NUMBER: _ClassVar[int]
    UINT32_VALUES_DEFAULT_FIELD_NUMBER: _ClassVar[int]
    INT64_VALUES_DEFAULT_FIELD_NUMBER: _ClassVar[int]
    UINT64_VALUES_DEFAULT_FIELD_NUMBER: _ClassVar[int]
    ALIGNMENT_CHECK_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    bool_values: _containers.RepeatedScalarFieldContainer[bool]
    byte_values: _containers.RepeatedScalarFieldContainer[int]
    char_values: _containers.RepeatedScalarFieldContainer[int]
    float32_values: _containers.RepeatedScalarFieldContainer[float]
    float64_values: _containers.RepeatedScalarFieldContainer[float]
    int8_values: _containers.RepeatedScalarFieldContainer[int]
    uint8_values: _containers.RepeatedScalarFieldContainer[int]
    int16_values: _containers.RepeatedScalarFieldContainer[int]
    uint16_values: _containers.RepeatedScalarFieldContainer[int]
    int32_values: _containers.RepeatedScalarFieldContainer[int]
    uint32_values: _containers.RepeatedScalarFieldContainer[int]
    int64_values: _containers.RepeatedScalarFieldContainer[int]
    uint64_values: _containers.RepeatedScalarFieldContainer[int]
    basic_types_values: _containers.RepeatedCompositeFieldContainer[_basic_types_pb2.BasicTypes]
    constants_values: _containers.RepeatedCompositeFieldContainer[_constants_pb2.Constants]
    defaults_values: _containers.RepeatedCompositeFieldContainer[_defaults_pb2.Defaults]
    bool_values_default: _containers.RepeatedScalarFieldContainer[bool]
    byte_values_default: _containers.RepeatedScalarFieldContainer[int]
    char_values_default: _containers.RepeatedScalarFieldContainer[int]
    float32_values_default: _containers.RepeatedScalarFieldContainer[float]
    float64_values_default: _containers.RepeatedScalarFieldContainer[float]
    int8_values_default: _containers.RepeatedScalarFieldContainer[int]
    uint8_values_default: _containers.RepeatedScalarFieldContainer[int]
    int16_values_default: _containers.RepeatedScalarFieldContainer[int]
    uint16_values_default: _containers.RepeatedScalarFieldContainer[int]
    int32_values_default: _containers.RepeatedScalarFieldContainer[int]
    uint32_values_default: _containers.RepeatedScalarFieldContainer[int]
    int64_values_default: _containers.RepeatedScalarFieldContainer[int]
    uint64_values_default: _containers.RepeatedScalarFieldContainer[int]
    alignment_check: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., bool_values: _Optional[_Iterable[bool]] = ..., byte_values: _Optional[_Iterable[int]] = ..., char_values: _Optional[_Iterable[int]] = ..., float32_values: _Optional[_Iterable[float]] = ..., float64_values: _Optional[_Iterable[float]] = ..., int8_values: _Optional[_Iterable[int]] = ..., uint8_values: _Optional[_Iterable[int]] = ..., int16_values: _Optional[_Iterable[int]] = ..., uint16_values: _Optional[_Iterable[int]] = ..., int32_values: _Optional[_Iterable[int]] = ..., uint32_values: _Optional[_Iterable[int]] = ..., int64_values: _Optional[_Iterable[int]] = ..., uint64_values: _Optional[_Iterable[int]] = ..., basic_types_values: _Optional[_Iterable[_Union[_basic_types_pb2.BasicTypes, _Mapping]]] = ..., constants_values: _Optional[_Iterable[_Union[_constants_pb2.Constants, _Mapping]]] = ..., defaults_values: _Optional[_Iterable[_Union[_defaults_pb2.Defaults, _Mapping]]] = ..., bool_values_default: _Optional[_Iterable[bool]] = ..., byte_values_default: _Optional[_Iterable[int]] = ..., char_values_default: _Optional[_Iterable[int]] = ..., float32_values_default: _Optional[_Iterable[float]] = ..., float64_values_default: _Optional[_Iterable[float]] = ..., int8_values_default: _Optional[_Iterable[int]] = ..., uint8_values_default: _Optional[_Iterable[int]] = ..., int16_values_default: _Optional[_Iterable[int]] = ..., uint16_values_default: _Optional[_Iterable[int]] = ..., int32_values_default: _Optional[_Iterable[int]] = ..., uint32_values_default: _Optional[_Iterable[int]] = ..., int64_values_default: _Optional[_Iterable[int]] = ..., uint64_values_default: _Optional[_Iterable[int]] = ..., alignment_check: _Optional[int] = ...) -> None: ...
