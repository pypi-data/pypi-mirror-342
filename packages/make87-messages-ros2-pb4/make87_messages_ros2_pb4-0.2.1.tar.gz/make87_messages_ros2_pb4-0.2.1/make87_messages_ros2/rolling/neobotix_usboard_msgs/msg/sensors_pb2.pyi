from make87_messages_ros2.rolling.neobotix_usboard_msgs.msg import sensor_data_pb2 as _sensor_data_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Sensors(_message.Message):
    __slots__ = ["header", "sensors"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SENSORS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    sensors: _containers.RepeatedCompositeFieldContainer[_sensor_data_pb2.SensorData]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., sensors: _Optional[_Iterable[_Union[_sensor_data_pb2.SensorData, _Mapping]]] = ...) -> None: ...
