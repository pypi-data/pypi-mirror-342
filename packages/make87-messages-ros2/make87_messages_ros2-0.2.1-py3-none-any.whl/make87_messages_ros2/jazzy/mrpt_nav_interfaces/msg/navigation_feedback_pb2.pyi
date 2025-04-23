from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class NavigationFeedback(_message.Message):
    __slots__ = ["total_waypoints", "reached_waypoints"]
    TOTAL_WAYPOINTS_FIELD_NUMBER: _ClassVar[int]
    REACHED_WAYPOINTS_FIELD_NUMBER: _ClassVar[int]
    total_waypoints: int
    reached_waypoints: int
    def __init__(self, total_waypoints: _Optional[int] = ..., reached_waypoints: _Optional[int] = ...) -> None: ...
