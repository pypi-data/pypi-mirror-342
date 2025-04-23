from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class LaneletPrimitive(_message.Message):
    __slots__ = ["id", "primitive_type"]
    ID_FIELD_NUMBER: _ClassVar[int]
    PRIMITIVE_TYPE_FIELD_NUMBER: _ClassVar[int]
    id: int
    primitive_type: str
    def __init__(self, id: _Optional[int] = ..., primitive_type: _Optional[str] = ...) -> None: ...
