from make87_messages_ros2.jazzy.rcl_interfaces.msg import logger_level_pb2 as _logger_level_pb2
from make87_messages_ros2.jazzy.rcl_interfaces.msg import set_logger_levels_result_pb2 as _set_logger_levels_result_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetLoggerLevelsRequest(_message.Message):
    __slots__ = ["levels"]
    LEVELS_FIELD_NUMBER: _ClassVar[int]
    levels: _containers.RepeatedCompositeFieldContainer[_logger_level_pb2.LoggerLevel]
    def __init__(self, levels: _Optional[_Iterable[_Union[_logger_level_pb2.LoggerLevel, _Mapping]]] = ...) -> None: ...

class SetLoggerLevelsResponse(_message.Message):
    __slots__ = ["results"]
    RESULTS_FIELD_NUMBER: _ClassVar[int]
    results: _containers.RepeatedCompositeFieldContainer[_set_logger_levels_result_pb2.SetLoggerLevelsResult]
    def __init__(self, results: _Optional[_Iterable[_Union[_set_logger_levels_result_pb2.SetLoggerLevelsResult, _Mapping]]] = ...) -> None: ...
