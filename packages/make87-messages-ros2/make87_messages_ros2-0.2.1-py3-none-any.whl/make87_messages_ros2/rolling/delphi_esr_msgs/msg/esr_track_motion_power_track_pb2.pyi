from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class EsrTrackMotionPowerTrack(_message.Message):
    __slots__ = ["id", "movable_fast", "movable_slow", "moving", "power"]
    ID_FIELD_NUMBER: _ClassVar[int]
    MOVABLE_FAST_FIELD_NUMBER: _ClassVar[int]
    MOVABLE_SLOW_FIELD_NUMBER: _ClassVar[int]
    MOVING_FIELD_NUMBER: _ClassVar[int]
    POWER_FIELD_NUMBER: _ClassVar[int]
    id: int
    movable_fast: bool
    movable_slow: bool
    moving: bool
    power: int
    def __init__(self, id: _Optional[int] = ..., movable_fast: bool = ..., movable_slow: bool = ..., moving: bool = ..., power: _Optional[int] = ...) -> None: ...
