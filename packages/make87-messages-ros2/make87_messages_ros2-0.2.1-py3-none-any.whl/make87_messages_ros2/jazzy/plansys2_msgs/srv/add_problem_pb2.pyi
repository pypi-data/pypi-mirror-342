from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AddProblemRequest(_message.Message):
    __slots__ = ["problem"]
    PROBLEM_FIELD_NUMBER: _ClassVar[int]
    problem: str
    def __init__(self, problem: _Optional[str] = ...) -> None: ...

class AddProblemResponse(_message.Message):
    __slots__ = ["success", "error_info"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_INFO_FIELD_NUMBER: _ClassVar[int]
    success: bool
    error_info: str
    def __init__(self, success: bool = ..., error_info: _Optional[str] = ...) -> None: ...
