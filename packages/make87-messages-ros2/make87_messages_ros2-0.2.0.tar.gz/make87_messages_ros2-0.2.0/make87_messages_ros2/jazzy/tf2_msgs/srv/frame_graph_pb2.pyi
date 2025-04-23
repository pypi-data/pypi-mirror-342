from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class FrameGraphRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class FrameGraphResponse(_message.Message):
    __slots__ = ["frame_yaml"]
    FRAME_YAML_FIELD_NUMBER: _ClassVar[int]
    frame_yaml: str
    def __init__(self, frame_yaml: _Optional[str] = ...) -> None: ...
