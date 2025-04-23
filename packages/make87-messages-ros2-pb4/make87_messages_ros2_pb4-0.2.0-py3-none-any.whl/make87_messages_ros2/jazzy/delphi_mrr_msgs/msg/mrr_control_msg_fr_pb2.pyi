from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MrrControlMsgFR(_message.Message):
    __slots__ = ["header", "can_sensitivity_profile_select", "can_stop_frequency_frml", "can_stop_frequency_frll", "can_prp_factor_frml", "can_prp_factor_frll", "can_desired_sweep_bw_frml", "can_desired_sweep_bw_frll"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CAN_SENSITIVITY_PROFILE_SELECT_FIELD_NUMBER: _ClassVar[int]
    CAN_STOP_FREQUENCY_FRML_FIELD_NUMBER: _ClassVar[int]
    CAN_STOP_FREQUENCY_FRLL_FIELD_NUMBER: _ClassVar[int]
    CAN_PRP_FACTOR_FRML_FIELD_NUMBER: _ClassVar[int]
    CAN_PRP_FACTOR_FRLL_FIELD_NUMBER: _ClassVar[int]
    CAN_DESIRED_SWEEP_BW_FRML_FIELD_NUMBER: _ClassVar[int]
    CAN_DESIRED_SWEEP_BW_FRLL_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    can_sensitivity_profile_select: int
    can_stop_frequency_frml: int
    can_stop_frequency_frll: int
    can_prp_factor_frml: float
    can_prp_factor_frll: float
    can_desired_sweep_bw_frml: int
    can_desired_sweep_bw_frll: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., can_sensitivity_profile_select: _Optional[int] = ..., can_stop_frequency_frml: _Optional[int] = ..., can_stop_frequency_frll: _Optional[int] = ..., can_prp_factor_frml: _Optional[float] = ..., can_prp_factor_frll: _Optional[float] = ..., can_desired_sweep_bw_frml: _Optional[int] = ..., can_desired_sweep_bw_frll: _Optional[int] = ...) -> None: ...
