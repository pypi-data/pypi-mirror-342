from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PlanningSceneComponents(_message.Message):
    __slots__ = ["components"]
    COMPONENTS_FIELD_NUMBER: _ClassVar[int]
    components: int
    def __init__(self, components: _Optional[int] = ...) -> None: ...
