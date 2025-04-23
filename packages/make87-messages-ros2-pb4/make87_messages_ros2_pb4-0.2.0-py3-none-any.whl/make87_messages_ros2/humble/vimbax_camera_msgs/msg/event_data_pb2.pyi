from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.vimbax_camera_msgs.msg import event_data_entry_pb2 as _event_data_entry_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EventData(_message.Message):
    __slots__ = ["header", "entries"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ENTRIES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    entries: _containers.RepeatedCompositeFieldContainer[_event_data_entry_pb2.EventDataEntry]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., entries: _Optional[_Iterable[_Union[_event_data_entry_pb2.EventDataEntry, _Mapping]]] = ...) -> None: ...
