from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class VisionClass(_message.Message):
    __slots__ = ["class_id", "class_name"]
    CLASS_ID_FIELD_NUMBER: _ClassVar[int]
    CLASS_NAME_FIELD_NUMBER: _ClassVar[int]
    class_id: int
    class_name: str
    def __init__(self, class_id: _Optional[int] = ..., class_name: _Optional[str] = ...) -> None: ...
