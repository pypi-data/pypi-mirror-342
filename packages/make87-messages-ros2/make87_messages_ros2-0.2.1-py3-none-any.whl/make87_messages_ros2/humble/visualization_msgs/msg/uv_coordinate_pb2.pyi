from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UVCoordinate(_message.Message):
    __slots__ = ["header", "u", "v"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    U_FIELD_NUMBER: _ClassVar[int]
    V_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    u: float
    v: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., u: _Optional[float] = ..., v: _Optional[float] = ...) -> None: ...
