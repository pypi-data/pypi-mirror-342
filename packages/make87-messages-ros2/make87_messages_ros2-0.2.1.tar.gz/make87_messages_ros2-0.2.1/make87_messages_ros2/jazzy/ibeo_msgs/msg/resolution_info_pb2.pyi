from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ResolutionInfo(_message.Message):
    __slots__ = ["resolution_start_angle", "resolution"]
    RESOLUTION_START_ANGLE_FIELD_NUMBER: _ClassVar[int]
    RESOLUTION_FIELD_NUMBER: _ClassVar[int]
    resolution_start_angle: float
    resolution: float
    def __init__(self, resolution_start_angle: _Optional[float] = ..., resolution: _Optional[float] = ...) -> None: ...
