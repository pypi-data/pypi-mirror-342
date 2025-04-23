from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class FileTruncateRequest(_message.Message):
    __slots__ = ["file_path", "length"]
    FILE_PATH_FIELD_NUMBER: _ClassVar[int]
    LENGTH_FIELD_NUMBER: _ClassVar[int]
    file_path: str
    length: int
    def __init__(self, file_path: _Optional[str] = ..., length: _Optional[int] = ...) -> None: ...

class FileTruncateResponse(_message.Message):
    __slots__ = ["success", "r_errno"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    R_ERRNO_FIELD_NUMBER: _ClassVar[int]
    success: bool
    r_errno: int
    def __init__(self, success: bool = ..., r_errno: _Optional[int] = ...) -> None: ...
