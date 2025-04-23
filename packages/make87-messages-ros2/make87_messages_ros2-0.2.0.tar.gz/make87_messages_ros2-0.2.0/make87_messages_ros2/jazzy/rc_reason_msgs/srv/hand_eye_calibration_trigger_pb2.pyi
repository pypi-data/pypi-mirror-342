from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class HandEyeCalibrationTriggerRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class HandEyeCalibrationTriggerResponse(_message.Message):
    __slots__ = ["success", "status", "message"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    status: int
    message: str
    def __init__(self, success: bool = ..., status: _Optional[int] = ..., message: _Optional[str] = ...) -> None: ...
