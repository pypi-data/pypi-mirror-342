from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class DeleteLightRequest(_message.Message):
    __slots__ = ["light_name"]
    LIGHT_NAME_FIELD_NUMBER: _ClassVar[int]
    light_name: str
    def __init__(self, light_name: _Optional[str] = ...) -> None: ...

class DeleteLightResponse(_message.Message):
    __slots__ = ["success", "status_message"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    status_message: str
    def __init__(self, success: bool = ..., status_message: _Optional[str] = ...) -> None: ...
