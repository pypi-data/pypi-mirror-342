from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class FloatingPointRange(_message.Message):
    __slots__ = ["from_value", "to_value", "step"]
    FROM_VALUE_FIELD_NUMBER: _ClassVar[int]
    TO_VALUE_FIELD_NUMBER: _ClassVar[int]
    STEP_FIELD_NUMBER: _ClassVar[int]
    from_value: float
    to_value: float
    step: float
    def __init__(self, from_value: _Optional[float] = ..., to_value: _Optional[float] = ..., step: _Optional[float] = ...) -> None: ...
