from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RobotInfo16(_message.Message):
    __slots__ = ["penalty", "secs_till_unpenalised"]
    PENALTY_FIELD_NUMBER: _ClassVar[int]
    SECS_TILL_UNPENALISED_FIELD_NUMBER: _ClassVar[int]
    penalty: int
    secs_till_unpenalised: int
    def __init__(self, penalty: _Optional[int] = ..., secs_till_unpenalised: _Optional[int] = ...) -> None: ...
