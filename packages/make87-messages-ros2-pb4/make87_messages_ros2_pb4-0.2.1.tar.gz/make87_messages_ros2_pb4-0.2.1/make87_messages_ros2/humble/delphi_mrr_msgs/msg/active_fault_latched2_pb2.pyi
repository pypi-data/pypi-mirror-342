from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ActiveFaultLatched2(_message.Message):
    __slots__ = ["header", "ros2_header", "ipma_pcan_data_range_check", "ipma_pcan_missing_msg", "vin_signal_compare_failure", "module_not_configured_error", "car_cfg_not_configured_error"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    IPMA_PCAN_DATA_RANGE_CHECK_FIELD_NUMBER: _ClassVar[int]
    IPMA_PCAN_MISSING_MSG_FIELD_NUMBER: _ClassVar[int]
    VIN_SIGNAL_COMPARE_FAILURE_FIELD_NUMBER: _ClassVar[int]
    MODULE_NOT_CONFIGURED_ERROR_FIELD_NUMBER: _ClassVar[int]
    CAR_CFG_NOT_CONFIGURED_ERROR_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    ipma_pcan_data_range_check: bool
    ipma_pcan_missing_msg: bool
    vin_signal_compare_failure: bool
    module_not_configured_error: bool
    car_cfg_not_configured_error: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., ipma_pcan_data_range_check: bool = ..., ipma_pcan_missing_msg: bool = ..., vin_signal_compare_failure: bool = ..., module_not_configured_error: bool = ..., car_cfg_not_configured_error: bool = ...) -> None: ...
