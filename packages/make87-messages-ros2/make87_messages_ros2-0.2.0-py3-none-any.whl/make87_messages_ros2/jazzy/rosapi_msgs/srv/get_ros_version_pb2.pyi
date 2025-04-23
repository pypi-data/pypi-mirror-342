from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GetROSVersionRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetROSVersionResponse(_message.Message):
    __slots__ = ["version", "distro"]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    DISTRO_FIELD_NUMBER: _ClassVar[int]
    version: int
    distro: str
    def __init__(self, version: _Optional[int] = ..., distro: _Optional[str] = ...) -> None: ...
