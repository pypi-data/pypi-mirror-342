from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StationManagerControlProtocolRequest(_message.Message):
    __slots__ = ["header", "request", "addition"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    ADDITION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    request: str
    addition: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., request: _Optional[str] = ..., addition: _Optional[str] = ...) -> None: ...

class StationManagerControlProtocolResponse(_message.Message):
    __slots__ = ["header", "response"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    response: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., response: _Optional[str] = ...) -> None: ...
