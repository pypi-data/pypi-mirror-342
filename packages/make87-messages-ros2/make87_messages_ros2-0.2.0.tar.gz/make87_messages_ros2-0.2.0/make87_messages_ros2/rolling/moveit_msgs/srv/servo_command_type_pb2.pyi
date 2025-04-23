from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ServoCommandTypeRequest(_message.Message):
    __slots__ = ["command_type"]
    COMMAND_TYPE_FIELD_NUMBER: _ClassVar[int]
    command_type: int
    def __init__(self, command_type: _Optional[int] = ...) -> None: ...

class ServoCommandTypeResponse(_message.Message):
    __slots__ = ["success"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
