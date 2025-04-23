from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Ptz(_message.Message):
    __slots__ = ["pan", "tilt", "zoom"]
    PAN_FIELD_NUMBER: _ClassVar[int]
    TILT_FIELD_NUMBER: _ClassVar[int]
    ZOOM_FIELD_NUMBER: _ClassVar[int]
    pan: float
    tilt: float
    zoom: float
    def __init__(self, pan: _Optional[float] = ..., tilt: _Optional[float] = ..., zoom: _Optional[float] = ...) -> None: ...
