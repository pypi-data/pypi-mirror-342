from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SaveRecordedRouteRequest(_message.Message):
    __slots__ = ["name", "thumbnail"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    THUMBNAIL_FIELD_NUMBER: _ClassVar[int]
    name: str
    thumbnail: str
    def __init__(self, name: _Optional[str] = ..., thumbnail: _Optional[str] = ...) -> None: ...

class SaveRecordedRouteResponse(_message.Message):
    __slots__ = ["success", "message"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...
