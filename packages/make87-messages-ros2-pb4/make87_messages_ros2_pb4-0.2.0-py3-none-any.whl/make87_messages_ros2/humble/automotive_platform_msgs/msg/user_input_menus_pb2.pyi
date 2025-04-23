from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UserInputMenus(_message.Message):
    __slots__ = ["header", "ros2_header", "str_whl_left_btn_left", "str_whl_left_btn_down", "str_whl_left_btn_right", "str_whl_left_btn_up", "str_whl_left_btn_ok", "str_whl_right_btn_left", "str_whl_right_btn_down", "str_whl_right_btn_right", "str_whl_right_btn_up", "str_whl_right_btn_ok", "cntr_cons_btn_left", "cntr_cons_btn_down", "cntr_cons_btn_right", "cntr_cons_btn_up", "cntr_cons_btn_ok"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    STR_WHL_LEFT_BTN_LEFT_FIELD_NUMBER: _ClassVar[int]
    STR_WHL_LEFT_BTN_DOWN_FIELD_NUMBER: _ClassVar[int]
    STR_WHL_LEFT_BTN_RIGHT_FIELD_NUMBER: _ClassVar[int]
    STR_WHL_LEFT_BTN_UP_FIELD_NUMBER: _ClassVar[int]
    STR_WHL_LEFT_BTN_OK_FIELD_NUMBER: _ClassVar[int]
    STR_WHL_RIGHT_BTN_LEFT_FIELD_NUMBER: _ClassVar[int]
    STR_WHL_RIGHT_BTN_DOWN_FIELD_NUMBER: _ClassVar[int]
    STR_WHL_RIGHT_BTN_RIGHT_FIELD_NUMBER: _ClassVar[int]
    STR_WHL_RIGHT_BTN_UP_FIELD_NUMBER: _ClassVar[int]
    STR_WHL_RIGHT_BTN_OK_FIELD_NUMBER: _ClassVar[int]
    CNTR_CONS_BTN_LEFT_FIELD_NUMBER: _ClassVar[int]
    CNTR_CONS_BTN_DOWN_FIELD_NUMBER: _ClassVar[int]
    CNTR_CONS_BTN_RIGHT_FIELD_NUMBER: _ClassVar[int]
    CNTR_CONS_BTN_UP_FIELD_NUMBER: _ClassVar[int]
    CNTR_CONS_BTN_OK_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    str_whl_left_btn_left: bool
    str_whl_left_btn_down: bool
    str_whl_left_btn_right: bool
    str_whl_left_btn_up: bool
    str_whl_left_btn_ok: bool
    str_whl_right_btn_left: bool
    str_whl_right_btn_down: bool
    str_whl_right_btn_right: bool
    str_whl_right_btn_up: bool
    str_whl_right_btn_ok: bool
    cntr_cons_btn_left: bool
    cntr_cons_btn_down: bool
    cntr_cons_btn_right: bool
    cntr_cons_btn_up: bool
    cntr_cons_btn_ok: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., str_whl_left_btn_left: bool = ..., str_whl_left_btn_down: bool = ..., str_whl_left_btn_right: bool = ..., str_whl_left_btn_up: bool = ..., str_whl_left_btn_ok: bool = ..., str_whl_right_btn_left: bool = ..., str_whl_right_btn_down: bool = ..., str_whl_right_btn_right: bool = ..., str_whl_right_btn_up: bool = ..., str_whl_right_btn_ok: bool = ..., cntr_cons_btn_left: bool = ..., cntr_cons_btn_down: bool = ..., cntr_cons_btn_right: bool = ..., cntr_cons_btn_up: bool = ..., cntr_cons_btn_ok: bool = ...) -> None: ...
