from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SPLSM(_message.Message):
    __slots__ = ["player_num", "team_num", "fallen", "pose", "ball_age", "ball", "data"]
    PLAYER_NUM_FIELD_NUMBER: _ClassVar[int]
    TEAM_NUM_FIELD_NUMBER: _ClassVar[int]
    FALLEN_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    BALL_AGE_FIELD_NUMBER: _ClassVar[int]
    BALL_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    player_num: int
    team_num: int
    fallen: int
    pose: _containers.RepeatedScalarFieldContainer[float]
    ball_age: float
    ball: _containers.RepeatedScalarFieldContainer[float]
    data: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, player_num: _Optional[int] = ..., team_num: _Optional[int] = ..., fallen: _Optional[int] = ..., pose: _Optional[_Iterable[float]] = ..., ball_age: _Optional[float] = ..., ball: _Optional[_Iterable[float]] = ..., data: _Optional[_Iterable[int]] = ...) -> None: ...
