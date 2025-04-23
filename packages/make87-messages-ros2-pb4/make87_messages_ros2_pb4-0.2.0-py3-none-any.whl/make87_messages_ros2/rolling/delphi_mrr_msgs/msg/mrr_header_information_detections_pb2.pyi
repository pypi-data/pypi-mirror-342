from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MrrHeaderInformationDetections(_message.Message):
    __slots__ = ["header", "can_align_updates_done", "can_scan_index", "can_number_of_det", "can_look_id", "can_look_index"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CAN_ALIGN_UPDATES_DONE_FIELD_NUMBER: _ClassVar[int]
    CAN_SCAN_INDEX_FIELD_NUMBER: _ClassVar[int]
    CAN_NUMBER_OF_DET_FIELD_NUMBER: _ClassVar[int]
    CAN_LOOK_ID_FIELD_NUMBER: _ClassVar[int]
    CAN_LOOK_INDEX_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    can_align_updates_done: int
    can_scan_index: int
    can_number_of_det: int
    can_look_id: int
    can_look_index: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., can_align_updates_done: _Optional[int] = ..., can_scan_index: _Optional[int] = ..., can_number_of_det: _Optional[int] = ..., can_look_id: _Optional[int] = ..., can_look_index: _Optional[int] = ...) -> None: ...
