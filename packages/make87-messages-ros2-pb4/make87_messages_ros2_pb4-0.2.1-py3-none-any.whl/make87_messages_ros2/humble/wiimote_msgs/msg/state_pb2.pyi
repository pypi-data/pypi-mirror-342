from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from make87_messages_ros2.humble.wiimote_msgs.msg import ir_source_info_pb2 as _ir_source_info_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class State(_message.Message):
    __slots__ = ["header", "ros2_header", "angular_velocity_zeroed", "angular_velocity_raw", "angular_velocity_covariance", "linear_acceleration_zeroed", "linear_acceleration_raw", "linear_acceleration_covariance", "nunchuk_acceleration_zeroed", "nunchuk_acceleration_raw", "nunchuk_joystick_zeroed", "nunchuk_joystick_raw", "buttons", "nunchuk_buttons", "leds", "rumble", "ir_tracking", "raw_battery", "percent_battery", "zeroing_time", "errors"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    ANGULAR_VELOCITY_ZEROED_FIELD_NUMBER: _ClassVar[int]
    ANGULAR_VELOCITY_RAW_FIELD_NUMBER: _ClassVar[int]
    ANGULAR_VELOCITY_COVARIANCE_FIELD_NUMBER: _ClassVar[int]
    LINEAR_ACCELERATION_ZEROED_FIELD_NUMBER: _ClassVar[int]
    LINEAR_ACCELERATION_RAW_FIELD_NUMBER: _ClassVar[int]
    LINEAR_ACCELERATION_COVARIANCE_FIELD_NUMBER: _ClassVar[int]
    NUNCHUK_ACCELERATION_ZEROED_FIELD_NUMBER: _ClassVar[int]
    NUNCHUK_ACCELERATION_RAW_FIELD_NUMBER: _ClassVar[int]
    NUNCHUK_JOYSTICK_ZEROED_FIELD_NUMBER: _ClassVar[int]
    NUNCHUK_JOYSTICK_RAW_FIELD_NUMBER: _ClassVar[int]
    BUTTONS_FIELD_NUMBER: _ClassVar[int]
    NUNCHUK_BUTTONS_FIELD_NUMBER: _ClassVar[int]
    LEDS_FIELD_NUMBER: _ClassVar[int]
    RUMBLE_FIELD_NUMBER: _ClassVar[int]
    IR_TRACKING_FIELD_NUMBER: _ClassVar[int]
    RAW_BATTERY_FIELD_NUMBER: _ClassVar[int]
    PERCENT_BATTERY_FIELD_NUMBER: _ClassVar[int]
    ZEROING_TIME_FIELD_NUMBER: _ClassVar[int]
    ERRORS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    angular_velocity_zeroed: _vector3_pb2.Vector3
    angular_velocity_raw: _vector3_pb2.Vector3
    angular_velocity_covariance: _containers.RepeatedScalarFieldContainer[float]
    linear_acceleration_zeroed: _vector3_pb2.Vector3
    linear_acceleration_raw: _vector3_pb2.Vector3
    linear_acceleration_covariance: _containers.RepeatedScalarFieldContainer[float]
    nunchuk_acceleration_zeroed: _vector3_pb2.Vector3
    nunchuk_acceleration_raw: _vector3_pb2.Vector3
    nunchuk_joystick_zeroed: _containers.RepeatedScalarFieldContainer[float]
    nunchuk_joystick_raw: _containers.RepeatedScalarFieldContainer[float]
    buttons: _containers.RepeatedScalarFieldContainer[bool]
    nunchuk_buttons: _containers.RepeatedScalarFieldContainer[bool]
    leds: _containers.RepeatedScalarFieldContainer[bool]
    rumble: bool
    ir_tracking: _containers.RepeatedCompositeFieldContainer[_ir_source_info_pb2.IrSourceInfo]
    raw_battery: float
    percent_battery: float
    zeroing_time: _time_pb2.Time
    errors: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., angular_velocity_zeroed: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., angular_velocity_raw: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., angular_velocity_covariance: _Optional[_Iterable[float]] = ..., linear_acceleration_zeroed: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., linear_acceleration_raw: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., linear_acceleration_covariance: _Optional[_Iterable[float]] = ..., nunchuk_acceleration_zeroed: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., nunchuk_acceleration_raw: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., nunchuk_joystick_zeroed: _Optional[_Iterable[float]] = ..., nunchuk_joystick_raw: _Optional[_Iterable[float]] = ..., buttons: _Optional[_Iterable[bool]] = ..., nunchuk_buttons: _Optional[_Iterable[bool]] = ..., leds: _Optional[_Iterable[bool]] = ..., rumble: bool = ..., ir_tracking: _Optional[_Iterable[_Union[_ir_source_info_pb2.IrSourceInfo, _Mapping]]] = ..., raw_battery: _Optional[float] = ..., percent_battery: _Optional[float] = ..., zeroing_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., errors: _Optional[int] = ...) -> None: ...
