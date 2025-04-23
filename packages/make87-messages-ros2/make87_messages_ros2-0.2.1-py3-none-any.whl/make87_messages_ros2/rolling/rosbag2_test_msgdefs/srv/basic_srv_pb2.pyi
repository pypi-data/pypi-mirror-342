from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class BasicSrvRequest(_message.Message):
    __slots__ = ["req"]
    REQ_FIELD_NUMBER: _ClassVar[int]
    req: str
    def __init__(self, req: _Optional[str] = ...) -> None: ...

class BasicSrvResponse(_message.Message):
    __slots__ = ["resp"]
    RESP_FIELD_NUMBER: _ClassVar[int]
    resp: str
    def __init__(self, resp: _Optional[str] = ...) -> None: ...
