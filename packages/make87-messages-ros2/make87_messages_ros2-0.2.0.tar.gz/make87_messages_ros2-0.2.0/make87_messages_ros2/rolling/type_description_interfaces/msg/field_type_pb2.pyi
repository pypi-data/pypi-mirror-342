from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class FieldType(_message.Message):
    __slots__ = ["type_id", "capacity", "string_capacity", "nested_type_name"]
    TYPE_ID_FIELD_NUMBER: _ClassVar[int]
    CAPACITY_FIELD_NUMBER: _ClassVar[int]
    STRING_CAPACITY_FIELD_NUMBER: _ClassVar[int]
    NESTED_TYPE_NAME_FIELD_NUMBER: _ClassVar[int]
    type_id: int
    capacity: int
    string_capacity: int
    nested_type_name: str
    def __init__(self, type_id: _Optional[int] = ..., capacity: _Optional[int] = ..., string_capacity: _Optional[int] = ..., nested_type_name: _Optional[str] = ...) -> None: ...
