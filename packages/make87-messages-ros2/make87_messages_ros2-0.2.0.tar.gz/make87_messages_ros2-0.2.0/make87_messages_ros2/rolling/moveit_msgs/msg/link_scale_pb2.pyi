from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class LinkScale(_message.Message):
    __slots__ = ["link_name", "scale"]
    LINK_NAME_FIELD_NUMBER: _ClassVar[int]
    SCALE_FIELD_NUMBER: _ClassVar[int]
    link_name: str
    scale: float
    def __init__(self, link_name: _Optional[str] = ..., scale: _Optional[float] = ...) -> None: ...
