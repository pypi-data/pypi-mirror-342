from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetPidRequest(_message.Message):
    __slots__ = ["header", "id", "max_repeats", "p", "i", "d"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    MAX_REPEATS_FIELD_NUMBER: _ClassVar[int]
    P_FIELD_NUMBER: _ClassVar[int]
    I_FIELD_NUMBER: _ClassVar[int]
    D_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    id: int
    max_repeats: int
    p: float
    i: float
    d: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., id: _Optional[int] = ..., max_repeats: _Optional[int] = ..., p: _Optional[float] = ..., i: _Optional[float] = ..., d: _Optional[float] = ...) -> None: ...

class SetPidResponse(_message.Message):
    __slots__ = ["header", "success", "failures"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    FAILURES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    failures: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., failures: _Optional[int] = ...) -> None: ...
