from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class EndpointDelRequest(_message.Message):
    __slots__ = ["id", "url", "type"]
    ID_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    id: int
    url: str
    type: int
    def __init__(self, id: _Optional[int] = ..., url: _Optional[str] = ..., type: _Optional[int] = ...) -> None: ...

class EndpointDelResponse(_message.Message):
    __slots__ = ["successful"]
    SUCCESSFUL_FIELD_NUMBER: _ClassVar[int]
    successful: bool
    def __init__(self, successful: bool = ...) -> None: ...
