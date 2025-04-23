from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RoutePrecondition(_message.Message):
    __slots__ = ["robot_id", "current_route_segment"]
    ROBOT_ID_FIELD_NUMBER: _ClassVar[int]
    CURRENT_ROUTE_SEGMENT_FIELD_NUMBER: _ClassVar[int]
    robot_id: str
    current_route_segment: int
    def __init__(self, robot_id: _Optional[str] = ..., current_route_segment: _Optional[int] = ...) -> None: ...
