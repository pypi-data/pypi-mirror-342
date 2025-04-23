from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Sigma2D(_message.Message):
    __slots__ = ["sigma_x", "sigma_y"]
    SIGMA_X_FIELD_NUMBER: _ClassVar[int]
    SIGMA_Y_FIELD_NUMBER: _ClassVar[int]
    sigma_x: int
    sigma_y: int
    def __init__(self, sigma_x: _Optional[int] = ..., sigma_y: _Optional[int] = ...) -> None: ...
