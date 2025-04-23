from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PlanItem(_message.Message):
    __slots__ = ["time", "action", "duration"]
    TIME_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    time: float
    action: str
    duration: float
    def __init__(self, time: _Optional[float] = ..., action: _Optional[str] = ..., duration: _Optional[float] = ...) -> None: ...
