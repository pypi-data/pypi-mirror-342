from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.as2_msgs.msg import control_mode_pb2 as _control_mode_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ControllerInfo(_message.Message):
    __slots__ = ["header", "ros2_header", "input_control_mode", "output_control_mode"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    INPUT_CONTROL_MODE_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_CONTROL_MODE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    input_control_mode: _control_mode_pb2.ControlMode
    output_control_mode: _control_mode_pb2.ControlMode
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., input_control_mode: _Optional[_Union[_control_mode_pb2.ControlMode, _Mapping]] = ..., output_control_mode: _Optional[_Union[_control_mode_pb2.ControlMode, _Mapping]] = ...) -> None: ...
