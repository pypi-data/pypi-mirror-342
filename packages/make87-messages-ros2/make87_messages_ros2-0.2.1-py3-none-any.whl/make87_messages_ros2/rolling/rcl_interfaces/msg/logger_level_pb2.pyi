from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class LoggerLevel(_message.Message):
    __slots__ = ["name", "level"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    name: str
    level: int
    def __init__(self, name: _Optional[str] = ..., level: _Optional[int] = ...) -> None: ...
