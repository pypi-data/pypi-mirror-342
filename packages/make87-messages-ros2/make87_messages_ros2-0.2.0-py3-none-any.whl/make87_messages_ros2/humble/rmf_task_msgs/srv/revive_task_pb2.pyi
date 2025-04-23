from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ReviveTaskRequest(_message.Message):
    __slots__ = ["header", "requester", "task_id"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    REQUESTER_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    requester: str
    task_id: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., requester: _Optional[str] = ..., task_id: _Optional[str] = ...) -> None: ...

class ReviveTaskResponse(_message.Message):
    __slots__ = ["header", "success"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ...) -> None: ...
