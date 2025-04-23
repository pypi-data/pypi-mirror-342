from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Property(_message.Message):
    __slots__ = ["property", "anything"]
    PROPERTY_FIELD_NUMBER: _ClassVar[int]
    ANYTHING_FIELD_NUMBER: _ClassVar[int]
    property: str
    anything: str
    def __init__(self, property: _Optional[str] = ..., anything: _Optional[str] = ...) -> None: ...
