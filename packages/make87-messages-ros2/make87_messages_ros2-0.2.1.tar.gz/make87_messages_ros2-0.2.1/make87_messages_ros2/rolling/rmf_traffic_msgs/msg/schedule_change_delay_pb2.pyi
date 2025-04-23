from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ScheduleChangeDelay(_message.Message):
    __slots__ = ["delay"]
    DELAY_FIELD_NUMBER: _ClassVar[int]
    delay: int
    def __init__(self, delay: _Optional[int] = ...) -> None: ...
