from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class PointField(_message.Message):
    __slots__ = ["name", "offset", "datatype", "count"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    DATATYPE_FIELD_NUMBER: _ClassVar[int]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    name: str
    offset: int
    datatype: int
    count: int
    def __init__(self, name: _Optional[str] = ..., offset: _Optional[int] = ..., datatype: _Optional[int] = ..., count: _Optional[int] = ...) -> None: ...
