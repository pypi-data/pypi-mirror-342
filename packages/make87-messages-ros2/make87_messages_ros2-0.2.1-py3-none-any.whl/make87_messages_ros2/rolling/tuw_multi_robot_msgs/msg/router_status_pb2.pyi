from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RouterStatus(_message.Message):
    __slots__ = ["id", "success", "missing_robots", "duration", "overall_path_length", "longest_path_length", "priority_scheduling_attemps", "speed_scheduling_attemps"]
    ID_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MISSING_ROBOTS_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    OVERALL_PATH_LENGTH_FIELD_NUMBER: _ClassVar[int]
    LONGEST_PATH_LENGTH_FIELD_NUMBER: _ClassVar[int]
    PRIORITY_SCHEDULING_ATTEMPS_FIELD_NUMBER: _ClassVar[int]
    SPEED_SCHEDULING_ATTEMPS_FIELD_NUMBER: _ClassVar[int]
    id: int
    success: bool
    missing_robots: _containers.RepeatedScalarFieldContainer[str]
    duration: int
    overall_path_length: int
    longest_path_length: int
    priority_scheduling_attemps: int
    speed_scheduling_attemps: int
    def __init__(self, id: _Optional[int] = ..., success: bool = ..., missing_robots: _Optional[_Iterable[str]] = ..., duration: _Optional[int] = ..., overall_path_length: _Optional[int] = ..., longest_path_length: _Optional[int] = ..., priority_scheduling_attemps: _Optional[int] = ..., speed_scheduling_attemps: _Optional[int] = ...) -> None: ...
