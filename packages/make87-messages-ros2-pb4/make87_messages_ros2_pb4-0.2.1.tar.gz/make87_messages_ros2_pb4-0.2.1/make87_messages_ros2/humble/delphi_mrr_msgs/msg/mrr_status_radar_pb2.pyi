from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MrrStatusRadar(_message.Message):
    __slots__ = ["header", "ros2_header", "can_interference_type", "can_recommend_unconverge", "can_blockage_sidelobe_filter_val", "can_radar_align_incomplete", "can_blockage_sidelobe", "can_blockage_mnr", "can_radar_ext_cond_nok", "can_radar_align_out_range", "can_radar_align_not_start", "can_radar_overheat_error", "can_radar_not_op", "can_xcvr_operational"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    CAN_INTERFERENCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    CAN_RECOMMEND_UNCONVERGE_FIELD_NUMBER: _ClassVar[int]
    CAN_BLOCKAGE_SIDELOBE_FILTER_VAL_FIELD_NUMBER: _ClassVar[int]
    CAN_RADAR_ALIGN_INCOMPLETE_FIELD_NUMBER: _ClassVar[int]
    CAN_BLOCKAGE_SIDELOBE_FIELD_NUMBER: _ClassVar[int]
    CAN_BLOCKAGE_MNR_FIELD_NUMBER: _ClassVar[int]
    CAN_RADAR_EXT_COND_NOK_FIELD_NUMBER: _ClassVar[int]
    CAN_RADAR_ALIGN_OUT_RANGE_FIELD_NUMBER: _ClassVar[int]
    CAN_RADAR_ALIGN_NOT_START_FIELD_NUMBER: _ClassVar[int]
    CAN_RADAR_OVERHEAT_ERROR_FIELD_NUMBER: _ClassVar[int]
    CAN_RADAR_NOT_OP_FIELD_NUMBER: _ClassVar[int]
    CAN_XCVR_OPERATIONAL_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    can_interference_type: int
    can_recommend_unconverge: bool
    can_blockage_sidelobe_filter_val: int
    can_radar_align_incomplete: bool
    can_blockage_sidelobe: bool
    can_blockage_mnr: bool
    can_radar_ext_cond_nok: bool
    can_radar_align_out_range: bool
    can_radar_align_not_start: bool
    can_radar_overheat_error: bool
    can_radar_not_op: bool
    can_xcvr_operational: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., can_interference_type: _Optional[int] = ..., can_recommend_unconverge: bool = ..., can_blockage_sidelobe_filter_val: _Optional[int] = ..., can_radar_align_incomplete: bool = ..., can_blockage_sidelobe: bool = ..., can_blockage_mnr: bool = ..., can_radar_ext_cond_nok: bool = ..., can_radar_align_out_range: bool = ..., can_radar_align_not_start: bool = ..., can_radar_overheat_error: bool = ..., can_radar_not_op: bool = ..., can_xcvr_operational: bool = ...) -> None: ...
