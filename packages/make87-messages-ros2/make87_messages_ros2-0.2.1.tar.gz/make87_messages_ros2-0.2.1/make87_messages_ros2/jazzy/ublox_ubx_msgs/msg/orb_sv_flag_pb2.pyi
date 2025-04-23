from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class OrbSVFlag(_message.Message):
    __slots__ = ["health", "visibility"]
    HEALTH_FIELD_NUMBER: _ClassVar[int]
    VISIBILITY_FIELD_NUMBER: _ClassVar[int]
    health: int
    visibility: int
    def __init__(self, health: _Optional[int] = ..., visibility: _Optional[int] = ...) -> None: ...
