from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SpeedLimitedLane(_message.Message):
    __slots__ = ["lane_index", "speed_limit"]
    LANE_INDEX_FIELD_NUMBER: _ClassVar[int]
    SPEED_LIMIT_FIELD_NUMBER: _ClassVar[int]
    lane_index: int
    speed_limit: float
    def __init__(self, lane_index: _Optional[int] = ..., speed_limit: _Optional[float] = ...) -> None: ...
