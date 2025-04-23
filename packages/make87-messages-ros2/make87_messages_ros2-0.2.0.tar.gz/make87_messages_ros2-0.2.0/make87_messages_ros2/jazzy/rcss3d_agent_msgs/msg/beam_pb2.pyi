from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Beam(_message.Message):
    __slots__ = ["x", "y", "rot"]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    ROT_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    rot: float
    def __init__(self, x: _Optional[float] = ..., y: _Optional[float] = ..., rot: _Optional[float] = ...) -> None: ...
