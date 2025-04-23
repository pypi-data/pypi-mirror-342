from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class MessageIntervalRequest(_message.Message):
    __slots__ = ["message_id", "message_rate"]
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_RATE_FIELD_NUMBER: _ClassVar[int]
    message_id: int
    message_rate: float
    def __init__(self, message_id: _Optional[int] = ..., message_rate: _Optional[float] = ...) -> None: ...

class MessageIntervalResponse(_message.Message):
    __slots__ = ["success"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
