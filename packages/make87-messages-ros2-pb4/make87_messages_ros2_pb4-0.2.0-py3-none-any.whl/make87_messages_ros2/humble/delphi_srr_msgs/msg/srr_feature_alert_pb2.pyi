from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SrrFeatureAlert(_message.Message):
    __slots__ = ["header", "ros2_header", "lcma_blis_ignored_track_id", "lcma_blis_track_id", "lcma_cvw_ttc", "cta_ttc_alert", "cta_selected_track_ttc", "cta_selected_track", "cta_alert", "cta_active", "lcma_cvw_cipv", "lcma_cvw_alert_state", "lcma_blis_alert_state", "lcma_active"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    LCMA_BLIS_IGNORED_TRACK_ID_FIELD_NUMBER: _ClassVar[int]
    LCMA_BLIS_TRACK_ID_FIELD_NUMBER: _ClassVar[int]
    LCMA_CVW_TTC_FIELD_NUMBER: _ClassVar[int]
    CTA_TTC_ALERT_FIELD_NUMBER: _ClassVar[int]
    CTA_SELECTED_TRACK_TTC_FIELD_NUMBER: _ClassVar[int]
    CTA_SELECTED_TRACK_FIELD_NUMBER: _ClassVar[int]
    CTA_ALERT_FIELD_NUMBER: _ClassVar[int]
    CTA_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    LCMA_CVW_CIPV_FIELD_NUMBER: _ClassVar[int]
    LCMA_CVW_ALERT_STATE_FIELD_NUMBER: _ClassVar[int]
    LCMA_BLIS_ALERT_STATE_FIELD_NUMBER: _ClassVar[int]
    LCMA_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    lcma_blis_ignored_track_id: int
    lcma_blis_track_id: int
    lcma_cvw_ttc: float
    cta_ttc_alert: bool
    cta_selected_track_ttc: float
    cta_selected_track: int
    cta_alert: int
    cta_active: bool
    lcma_cvw_cipv: int
    lcma_cvw_alert_state: int
    lcma_blis_alert_state: int
    lcma_active: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., lcma_blis_ignored_track_id: _Optional[int] = ..., lcma_blis_track_id: _Optional[int] = ..., lcma_cvw_ttc: _Optional[float] = ..., cta_ttc_alert: bool = ..., cta_selected_track_ttc: _Optional[float] = ..., cta_selected_track: _Optional[int] = ..., cta_alert: _Optional[int] = ..., cta_active: bool = ..., lcma_cvw_cipv: _Optional[int] = ..., lcma_cvw_alert_state: _Optional[int] = ..., lcma_blis_alert_state: _Optional[int] = ..., lcma_active: bool = ...) -> None: ...
