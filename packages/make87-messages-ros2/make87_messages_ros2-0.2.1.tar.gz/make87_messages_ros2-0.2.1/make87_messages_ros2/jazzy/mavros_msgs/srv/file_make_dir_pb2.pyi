from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class FileMakeDirRequest(_message.Message):
    __slots__ = ["dir_path"]
    DIR_PATH_FIELD_NUMBER: _ClassVar[int]
    dir_path: str
    def __init__(self, dir_path: _Optional[str] = ...) -> None: ...

class FileMakeDirResponse(_message.Message):
    __slots__ = ["success", "r_errno"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    R_ERRNO_FIELD_NUMBER: _ClassVar[int]
    success: bool
    r_errno: int
    def __init__(self, success: bool = ..., r_errno: _Optional[int] = ...) -> None: ...
