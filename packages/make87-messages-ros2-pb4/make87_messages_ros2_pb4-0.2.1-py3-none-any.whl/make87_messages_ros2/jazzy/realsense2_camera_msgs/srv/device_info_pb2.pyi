from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DeviceInfoRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class DeviceInfoResponse(_message.Message):
    __slots__ = ["device_name", "serial_number", "firmware_version", "usb_type_descriptor", "firmware_update_id", "sensors", "physical_port"]
    DEVICE_NAME_FIELD_NUMBER: _ClassVar[int]
    SERIAL_NUMBER_FIELD_NUMBER: _ClassVar[int]
    FIRMWARE_VERSION_FIELD_NUMBER: _ClassVar[int]
    USB_TYPE_DESCRIPTOR_FIELD_NUMBER: _ClassVar[int]
    FIRMWARE_UPDATE_ID_FIELD_NUMBER: _ClassVar[int]
    SENSORS_FIELD_NUMBER: _ClassVar[int]
    PHYSICAL_PORT_FIELD_NUMBER: _ClassVar[int]
    device_name: str
    serial_number: str
    firmware_version: str
    usb_type_descriptor: str
    firmware_update_id: str
    sensors: str
    physical_port: str
    def __init__(self, device_name: _Optional[str] = ..., serial_number: _Optional[str] = ..., firmware_version: _Optional[str] = ..., usb_type_descriptor: _Optional[str] = ..., firmware_update_id: _Optional[str] = ..., sensors: _Optional[str] = ..., physical_port: _Optional[str] = ...) -> None: ...
