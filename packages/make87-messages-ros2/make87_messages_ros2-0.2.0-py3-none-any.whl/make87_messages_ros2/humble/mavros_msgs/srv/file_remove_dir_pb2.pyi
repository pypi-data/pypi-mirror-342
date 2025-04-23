from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FileRemoveDirRequest(_message.Message):
    __slots__ = ["header", "dir_path"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DIR_PATH_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    dir_path: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., dir_path: _Optional[str] = ...) -> None: ...

class FileRemoveDirResponse(_message.Message):
    __slots__ = ["header", "success", "r_errno"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    R_ERRNO_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    r_errno: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., r_errno: _Optional[int] = ...) -> None: ...
