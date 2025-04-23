from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PtzState(_message.Message):
    __slots__ = ["mode", "pan", "tilt", "zoom"]
    MODE_FIELD_NUMBER: _ClassVar[int]
    PAN_FIELD_NUMBER: _ClassVar[int]
    TILT_FIELD_NUMBER: _ClassVar[int]
    ZOOM_FIELD_NUMBER: _ClassVar[int]
    mode: int
    pan: float
    tilt: float
    zoom: float
    def __init__(self, mode: _Optional[int] = ..., pan: _Optional[float] = ..., tilt: _Optional[float] = ..., zoom: _Optional[float] = ...) -> None: ...
