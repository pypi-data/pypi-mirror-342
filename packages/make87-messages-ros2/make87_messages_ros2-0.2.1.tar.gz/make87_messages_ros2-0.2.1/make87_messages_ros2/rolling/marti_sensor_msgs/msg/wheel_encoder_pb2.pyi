from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class WheelEncoder(_message.Message):
    __slots__ = ["frequency", "directional", "id"]
    FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    DIRECTIONAL_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    frequency: float
    directional: bool
    id: int
    def __init__(self, frequency: _Optional[float] = ..., directional: bool = ..., id: _Optional[int] = ...) -> None: ...
