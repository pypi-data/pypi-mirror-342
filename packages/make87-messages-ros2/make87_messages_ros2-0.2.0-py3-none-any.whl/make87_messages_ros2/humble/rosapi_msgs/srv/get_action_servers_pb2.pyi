from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetActionServersRequest(_message.Message):
    __slots__ = ["header"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...

class GetActionServersResponse(_message.Message):
    __slots__ = ["header", "action_servers"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ACTION_SERVERS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    action_servers: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., action_servers: _Optional[_Iterable[str]] = ...) -> None: ...
