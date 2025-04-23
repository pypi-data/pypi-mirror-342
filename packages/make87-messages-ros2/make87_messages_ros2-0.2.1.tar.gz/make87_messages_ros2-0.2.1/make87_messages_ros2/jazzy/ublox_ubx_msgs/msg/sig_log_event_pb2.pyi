from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SigLogEvent(_message.Message):
    __slots__ = ["time_elapsed", "detection_type", "event_type"]
    TIME_ELAPSED_FIELD_NUMBER: _ClassVar[int]
    DETECTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    EVENT_TYPE_FIELD_NUMBER: _ClassVar[int]
    time_elapsed: int
    detection_type: int
    event_type: int
    def __init__(self, time_elapsed: _Optional[int] = ..., detection_type: _Optional[int] = ..., event_type: _Optional[int] = ...) -> None: ...
