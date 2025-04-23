from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ButtonEvent(_message.Message):
    __slots__ = ["button", "state"]
    BUTTON_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    button: int
    state: int
    def __init__(self, button: _Optional[int] = ..., state: _Optional[int] = ...) -> None: ...
