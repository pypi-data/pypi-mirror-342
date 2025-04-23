from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NodeDetailsRequest(_message.Message):
    __slots__ = ["header", "node"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NODE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    node: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., node: _Optional[str] = ...) -> None: ...

class NodeDetailsResponse(_message.Message):
    __slots__ = ["header", "subscribing", "publishing", "services"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUBSCRIBING_FIELD_NUMBER: _ClassVar[int]
    PUBLISHING_FIELD_NUMBER: _ClassVar[int]
    SERVICES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    subscribing: _containers.RepeatedScalarFieldContainer[str]
    publishing: _containers.RepeatedScalarFieldContainer[str]
    services: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., subscribing: _Optional[_Iterable[str]] = ..., publishing: _Optional[_Iterable[str]] = ..., services: _Optional[_Iterable[str]] = ...) -> None: ...
