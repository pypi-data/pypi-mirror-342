from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DiagnosticsEthernetConfigurationInformation(_message.Message):
    __slots__ = ["header", "ip_address", "netmask", "vlan", "port"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    NETMASK_FIELD_NUMBER: _ClassVar[int]
    VLAN_FIELD_NUMBER: _ClassVar[int]
    PORT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ip_address: str
    netmask: str
    vlan: int
    port: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ip_address: _Optional[str] = ..., netmask: _Optional[str] = ..., vlan: _Optional[int] = ..., port: _Optional[int] = ...) -> None: ...
