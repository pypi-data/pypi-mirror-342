from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.sick_safetyscanners2_interfaces.msg import field_pb2 as _field_pb2
from make87_messages_ros2.humble.sick_safetyscanners2_interfaces.msg import monitoring_case_pb2 as _monitoring_case_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FieldDataRequest(_message.Message):
    __slots__ = ["header"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...

class FieldDataResponse(_message.Message):
    __slots__ = ["header", "fields", "device_name", "monitoring_cases"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    DEVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    MONITORING_CASES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    fields: _containers.RepeatedCompositeFieldContainer[_field_pb2.Field]
    device_name: str
    monitoring_cases: _containers.RepeatedCompositeFieldContainer[_monitoring_case_pb2.MonitoringCase]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., fields: _Optional[_Iterable[_Union[_field_pb2.Field, _Mapping]]] = ..., device_name: _Optional[str] = ..., monitoring_cases: _Optional[_Iterable[_Union[_monitoring_case_pb2.MonitoringCase, _Mapping]]] = ...) -> None: ...
