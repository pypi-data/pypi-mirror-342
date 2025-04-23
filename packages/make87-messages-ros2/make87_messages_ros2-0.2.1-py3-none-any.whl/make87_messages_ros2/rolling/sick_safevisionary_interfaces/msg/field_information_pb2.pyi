from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class FieldInformation(_message.Message):
    __slots__ = ["field_id", "field_set_id", "field_result", "eval_method", "field_active"]
    FIELD_ID_FIELD_NUMBER: _ClassVar[int]
    FIELD_SET_ID_FIELD_NUMBER: _ClassVar[int]
    FIELD_RESULT_FIELD_NUMBER: _ClassVar[int]
    EVAL_METHOD_FIELD_NUMBER: _ClassVar[int]
    FIELD_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    field_id: int
    field_set_id: int
    field_result: int
    eval_method: int
    field_active: int
    def __init__(self, field_id: _Optional[int] = ..., field_set_id: _Optional[int] = ..., field_result: _Optional[int] = ..., eval_method: _Optional[int] = ..., field_active: _Optional[int] = ...) -> None: ...
