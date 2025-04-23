from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RadarPreHeaderStatusBlock(_message.Message):
    __slots__ = ["uitelegramcount", "uicyclecount", "udisystemcountscan", "udisystemcounttransmit", "uiinputs", "uioutputs"]
    UITELEGRAMCOUNT_FIELD_NUMBER: _ClassVar[int]
    UICYCLECOUNT_FIELD_NUMBER: _ClassVar[int]
    UDISYSTEMCOUNTSCAN_FIELD_NUMBER: _ClassVar[int]
    UDISYSTEMCOUNTTRANSMIT_FIELD_NUMBER: _ClassVar[int]
    UIINPUTS_FIELD_NUMBER: _ClassVar[int]
    UIOUTPUTS_FIELD_NUMBER: _ClassVar[int]
    uitelegramcount: int
    uicyclecount: int
    udisystemcountscan: int
    udisystemcounttransmit: int
    uiinputs: int
    uioutputs: int
    def __init__(self, uitelegramcount: _Optional[int] = ..., uicyclecount: _Optional[int] = ..., udisystemcountscan: _Optional[int] = ..., udisystemcounttransmit: _Optional[int] = ..., uiinputs: _Optional[int] = ..., uioutputs: _Optional[int] = ...) -> None: ...
