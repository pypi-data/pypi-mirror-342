from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SetLoggerLevelsResult(_message.Message):
    __slots__ = ["successful", "reason"]
    SUCCESSFUL_FIELD_NUMBER: _ClassVar[int]
    REASON_FIELD_NUMBER: _ClassVar[int]
    successful: bool
    reason: str
    def __init__(self, successful: bool = ..., reason: _Optional[str] = ...) -> None: ...
