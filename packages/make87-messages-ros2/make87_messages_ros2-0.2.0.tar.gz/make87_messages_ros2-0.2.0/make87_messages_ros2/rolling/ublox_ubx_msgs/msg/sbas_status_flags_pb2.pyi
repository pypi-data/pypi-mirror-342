from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SBASStatusFlags(_message.Message):
    __slots__ = ["integrity_used"]
    INTEGRITY_USED_FIELD_NUMBER: _ClassVar[int]
    integrity_used: int
    def __init__(self, integrity_used: _Optional[int] = ...) -> None: ...
