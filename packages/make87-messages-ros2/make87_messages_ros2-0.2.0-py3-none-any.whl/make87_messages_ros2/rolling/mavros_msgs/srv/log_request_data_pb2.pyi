from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class LogRequestDataRequest(_message.Message):
    __slots__ = ["id", "offset", "count"]
    ID_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    id: int
    offset: int
    count: int
    def __init__(self, id: _Optional[int] = ..., offset: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...

class LogRequestDataResponse(_message.Message):
    __slots__ = ["success"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
