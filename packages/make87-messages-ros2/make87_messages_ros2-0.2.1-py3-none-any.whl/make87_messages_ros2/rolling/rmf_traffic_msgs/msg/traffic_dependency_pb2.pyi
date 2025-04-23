from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class TrafficDependency(_message.Message):
    __slots__ = ["dependent_checkpoint", "on_participant", "on_plan", "on_route", "on_checkpoint"]
    DEPENDENT_CHECKPOINT_FIELD_NUMBER: _ClassVar[int]
    ON_PARTICIPANT_FIELD_NUMBER: _ClassVar[int]
    ON_PLAN_FIELD_NUMBER: _ClassVar[int]
    ON_ROUTE_FIELD_NUMBER: _ClassVar[int]
    ON_CHECKPOINT_FIELD_NUMBER: _ClassVar[int]
    dependent_checkpoint: int
    on_participant: int
    on_plan: int
    on_route: int
    on_checkpoint: int
    def __init__(self, dependent_checkpoint: _Optional[int] = ..., on_participant: _Optional[int] = ..., on_plan: _Optional[int] = ..., on_route: _Optional[int] = ..., on_checkpoint: _Optional[int] = ...) -> None: ...
