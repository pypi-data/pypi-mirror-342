from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Gear(_message.Message):
    __slots__ = ["gear"]
    GEAR_FIELD_NUMBER: _ClassVar[int]
    gear: int
    def __init__(self, gear: _Optional[int] = ...) -> None: ...
