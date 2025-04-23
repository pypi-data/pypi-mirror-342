from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ParamValue(_message.Message):
    __slots__ = ["integer", "real"]
    INTEGER_FIELD_NUMBER: _ClassVar[int]
    REAL_FIELD_NUMBER: _ClassVar[int]
    integer: int
    real: float
    def __init__(self, integer: _Optional[int] = ..., real: _Optional[float] = ...) -> None: ...
