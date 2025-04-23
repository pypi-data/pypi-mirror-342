from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rc_common_msgs.msg import return_code_pb2 as _return_code_pb2
from make87_messages_ros2.humble.rc_reason_msgs.msg import region_of_interest3_d_pb2 as _region_of_interest3_d_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetRegionsOfInterest3DRequest(_message.Message):
    __slots__ = ["header", "region_of_interest_ids"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    REGION_OF_INTEREST_IDS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    region_of_interest_ids: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., region_of_interest_ids: _Optional[_Iterable[str]] = ...) -> None: ...

class GetRegionsOfInterest3DResponse(_message.Message):
    __slots__ = ["header", "regions_of_interest", "return_code"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    REGIONS_OF_INTEREST_FIELD_NUMBER: _ClassVar[int]
    RETURN_CODE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    regions_of_interest: _containers.RepeatedCompositeFieldContainer[_region_of_interest3_d_pb2.RegionOfInterest3D]
    return_code: _return_code_pb2.ReturnCode
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., regions_of_interest: _Optional[_Iterable[_Union[_region_of_interest3_d_pb2.RegionOfInterest3D, _Mapping]]] = ..., return_code: _Optional[_Union[_return_code_pb2.ReturnCode, _Mapping]] = ...) -> None: ...
