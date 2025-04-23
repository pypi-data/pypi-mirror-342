from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ControllerInfo(_message.Message):
    __slots__ = ["type", "p_gain", "i_gain", "d_gain"]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    P_GAIN_FIELD_NUMBER: _ClassVar[int]
    I_GAIN_FIELD_NUMBER: _ClassVar[int]
    D_GAIN_FIELD_NUMBER: _ClassVar[int]
    type: int
    p_gain: float
    i_gain: float
    d_gain: float
    def __init__(self, type: _Optional[int] = ..., p_gain: _Optional[float] = ..., i_gain: _Optional[float] = ..., d_gain: _Optional[float] = ...) -> None: ...
