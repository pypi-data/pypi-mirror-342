from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GameState(_message.Message):
    __slots__ = ["time", "playmode", "score_left", "score_right"]
    TIME_FIELD_NUMBER: _ClassVar[int]
    PLAYMODE_FIELD_NUMBER: _ClassVar[int]
    SCORE_LEFT_FIELD_NUMBER: _ClassVar[int]
    SCORE_RIGHT_FIELD_NUMBER: _ClassVar[int]
    time: float
    playmode: str
    score_left: int
    score_right: int
    def __init__(self, time: _Optional[float] = ..., playmode: _Optional[str] = ..., score_left: _Optional[int] = ..., score_right: _Optional[int] = ...) -> None: ...
