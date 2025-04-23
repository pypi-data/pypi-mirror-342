from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DriverCommands(_message.Message):
    __slots__ = ["msg_counter", "engage", "disengage", "speed_up", "slow_down", "further", "closer", "right_turn", "left_turn"]
    MSG_COUNTER_FIELD_NUMBER: _ClassVar[int]
    ENGAGE_FIELD_NUMBER: _ClassVar[int]
    DISENGAGE_FIELD_NUMBER: _ClassVar[int]
    SPEED_UP_FIELD_NUMBER: _ClassVar[int]
    SLOW_DOWN_FIELD_NUMBER: _ClassVar[int]
    FURTHER_FIELD_NUMBER: _ClassVar[int]
    CLOSER_FIELD_NUMBER: _ClassVar[int]
    RIGHT_TURN_FIELD_NUMBER: _ClassVar[int]
    LEFT_TURN_FIELD_NUMBER: _ClassVar[int]
    msg_counter: int
    engage: int
    disengage: int
    speed_up: int
    slow_down: int
    further: int
    closer: int
    right_turn: int
    left_turn: int
    def __init__(self, msg_counter: _Optional[int] = ..., engage: _Optional[int] = ..., disengage: _Optional[int] = ..., speed_up: _Optional[int] = ..., slow_down: _Optional[int] = ..., further: _Optional[int] = ..., closer: _Optional[int] = ..., right_turn: _Optional[int] = ..., left_turn: _Optional[int] = ...) -> None: ...
