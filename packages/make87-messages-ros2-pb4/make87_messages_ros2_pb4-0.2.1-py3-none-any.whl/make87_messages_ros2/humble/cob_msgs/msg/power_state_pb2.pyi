from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PowerState(_message.Message):
    __slots__ = ["header", "ros2_header", "voltage", "current", "power_consumption", "remaining_capacity", "relative_remaining_capacity", "connected", "charging", "time_remaining", "temperature"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    VOLTAGE_FIELD_NUMBER: _ClassVar[int]
    CURRENT_FIELD_NUMBER: _ClassVar[int]
    POWER_CONSUMPTION_FIELD_NUMBER: _ClassVar[int]
    REMAINING_CAPACITY_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_REMAINING_CAPACITY_FIELD_NUMBER: _ClassVar[int]
    CONNECTED_FIELD_NUMBER: _ClassVar[int]
    CHARGING_FIELD_NUMBER: _ClassVar[int]
    TIME_REMAINING_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    voltage: float
    current: float
    power_consumption: float
    remaining_capacity: float
    relative_remaining_capacity: float
    connected: bool
    charging: bool
    time_remaining: float
    temperature: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., voltage: _Optional[float] = ..., current: _Optional[float] = ..., power_consumption: _Optional[float] = ..., remaining_capacity: _Optional[float] = ..., relative_remaining_capacity: _Optional[float] = ..., connected: bool = ..., charging: bool = ..., time_remaining: _Optional[float] = ..., temperature: _Optional[float] = ...) -> None: ...
