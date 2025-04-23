from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.vimbax_camera_msgs.msg import error_pb2 as _error_pb2
from make87_messages_ros2.humble.vimbax_camera_msgs.msg import feature_module_pb2 as _feature_module_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FeatureRawSetRequest(_message.Message):
    __slots__ = ["header", "feature_name", "feature_module", "buffer"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FEATURE_NAME_FIELD_NUMBER: _ClassVar[int]
    FEATURE_MODULE_FIELD_NUMBER: _ClassVar[int]
    BUFFER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    feature_name: str
    feature_module: _feature_module_pb2.FeatureModule
    buffer: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., feature_name: _Optional[str] = ..., feature_module: _Optional[_Union[_feature_module_pb2.FeatureModule, _Mapping]] = ..., buffer: _Optional[_Iterable[int]] = ...) -> None: ...

class FeatureRawSetResponse(_message.Message):
    __slots__ = ["header", "error"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    error: _error_pb2.Error
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., error: _Optional[_Union[_error_pb2.Error, _Mapping]] = ...) -> None: ...
