from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class NovatelPsrdop2System(_message.Message):
    __slots__ = ["system", "tdop"]
    SYSTEM_FIELD_NUMBER: _ClassVar[int]
    TDOP_FIELD_NUMBER: _ClassVar[int]
    system: str
    tdop: float
    def __init__(self, system: _Optional[str] = ..., tdop: _Optional[float] = ...) -> None: ...
