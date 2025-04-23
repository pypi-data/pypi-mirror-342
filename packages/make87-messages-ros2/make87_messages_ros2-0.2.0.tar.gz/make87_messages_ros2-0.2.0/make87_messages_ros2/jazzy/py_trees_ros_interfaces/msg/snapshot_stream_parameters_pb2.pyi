from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SnapshotStreamParameters(_message.Message):
    __slots__ = ["snapshot_period", "blackboard_data", "blackboard_activity"]
    SNAPSHOT_PERIOD_FIELD_NUMBER: _ClassVar[int]
    BLACKBOARD_DATA_FIELD_NUMBER: _ClassVar[int]
    BLACKBOARD_ACTIVITY_FIELD_NUMBER: _ClassVar[int]
    snapshot_period: float
    blackboard_data: bool
    blackboard_activity: bool
    def __init__(self, snapshot_period: _Optional[float] = ..., blackboard_data: bool = ..., blackboard_activity: bool = ...) -> None: ...
