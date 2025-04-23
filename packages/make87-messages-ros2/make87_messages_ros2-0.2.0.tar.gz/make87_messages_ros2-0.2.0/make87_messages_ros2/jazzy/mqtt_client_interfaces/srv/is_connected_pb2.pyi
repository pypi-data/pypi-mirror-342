from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class IsConnectedRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class IsConnectedResponse(_message.Message):
    __slots__ = ["connected"]
    CONNECTED_FIELD_NUMBER: _ClassVar[int]
    connected: bool
    def __init__(self, connected: bool = ...) -> None: ...
