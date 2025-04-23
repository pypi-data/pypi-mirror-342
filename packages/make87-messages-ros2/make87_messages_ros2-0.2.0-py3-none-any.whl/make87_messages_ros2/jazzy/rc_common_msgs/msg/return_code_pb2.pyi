from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ReturnCode(_message.Message):
    __slots__ = ["value", "message"]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    value: int
    message: str
    def __init__(self, value: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...
