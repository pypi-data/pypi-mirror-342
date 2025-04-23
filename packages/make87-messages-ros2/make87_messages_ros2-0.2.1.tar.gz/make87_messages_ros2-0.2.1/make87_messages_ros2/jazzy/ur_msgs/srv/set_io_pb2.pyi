from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SetIORequest(_message.Message):
    __slots__ = ["fun", "pin", "state"]
    FUN_FIELD_NUMBER: _ClassVar[int]
    PIN_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    fun: int
    pin: int
    state: float
    def __init__(self, fun: _Optional[int] = ..., pin: _Optional[int] = ..., state: _Optional[float] = ...) -> None: ...

class SetIOResponse(_message.Message):
    __slots__ = ["success"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
