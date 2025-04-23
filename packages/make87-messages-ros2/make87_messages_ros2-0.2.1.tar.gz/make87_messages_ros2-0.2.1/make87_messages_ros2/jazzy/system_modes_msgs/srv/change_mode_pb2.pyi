from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ChangeModeRequest(_message.Message):
    __slots__ = ["mode_name"]
    MODE_NAME_FIELD_NUMBER: _ClassVar[int]
    mode_name: str
    def __init__(self, mode_name: _Optional[str] = ...) -> None: ...

class ChangeModeResponse(_message.Message):
    __slots__ = ["success"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
