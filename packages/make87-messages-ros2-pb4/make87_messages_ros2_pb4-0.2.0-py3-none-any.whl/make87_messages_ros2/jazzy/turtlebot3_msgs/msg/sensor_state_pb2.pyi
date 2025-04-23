from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SensorState(_message.Message):
    __slots__ = ["header", "bumper", "cliff", "sonar", "illumination", "led", "button", "torque", "left_encoder", "right_encoder", "battery"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BUMPER_FIELD_NUMBER: _ClassVar[int]
    CLIFF_FIELD_NUMBER: _ClassVar[int]
    SONAR_FIELD_NUMBER: _ClassVar[int]
    ILLUMINATION_FIELD_NUMBER: _ClassVar[int]
    LED_FIELD_NUMBER: _ClassVar[int]
    BUTTON_FIELD_NUMBER: _ClassVar[int]
    TORQUE_FIELD_NUMBER: _ClassVar[int]
    LEFT_ENCODER_FIELD_NUMBER: _ClassVar[int]
    RIGHT_ENCODER_FIELD_NUMBER: _ClassVar[int]
    BATTERY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    bumper: int
    cliff: float
    sonar: float
    illumination: float
    led: int
    button: int
    torque: bool
    left_encoder: int
    right_encoder: int
    battery: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., bumper: _Optional[int] = ..., cliff: _Optional[float] = ..., sonar: _Optional[float] = ..., illumination: _Optional[float] = ..., led: _Optional[int] = ..., button: _Optional[int] = ..., torque: bool = ..., left_encoder: _Optional[int] = ..., right_encoder: _Optional[int] = ..., battery: _Optional[float] = ...) -> None: ...
