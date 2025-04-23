from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class WorldReset(_message.Message):
    __slots__ = ["all", "time_only", "model_only"]
    ALL_FIELD_NUMBER: _ClassVar[int]
    TIME_ONLY_FIELD_NUMBER: _ClassVar[int]
    MODEL_ONLY_FIELD_NUMBER: _ClassVar[int]
    all: bool
    time_only: bool
    model_only: bool
    def __init__(self, all: bool = ..., time_only: bool = ..., model_only: bool = ...) -> None: ...
