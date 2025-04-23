from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Spherical(_message.Message):
    __slots__ = ["r", "phi", "theta"]
    R_FIELD_NUMBER: _ClassVar[int]
    PHI_FIELD_NUMBER: _ClassVar[int]
    THETA_FIELD_NUMBER: _ClassVar[int]
    r: float
    phi: float
    theta: float
    def __init__(self, r: _Optional[float] = ..., phi: _Optional[float] = ..., theta: _Optional[float] = ...) -> None: ...
