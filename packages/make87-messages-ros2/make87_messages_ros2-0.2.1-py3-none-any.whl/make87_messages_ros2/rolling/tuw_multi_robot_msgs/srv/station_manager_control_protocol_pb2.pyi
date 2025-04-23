from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class StationManagerControlProtocolRequest(_message.Message):
    __slots__ = ["request", "addition"]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    ADDITION_FIELD_NUMBER: _ClassVar[int]
    request: str
    addition: str
    def __init__(self, request: _Optional[str] = ..., addition: _Optional[str] = ...) -> None: ...

class StationManagerControlProtocolResponse(_message.Message):
    __slots__ = ["response"]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    response: str
    def __init__(self, response: _Optional[str] = ...) -> None: ...
