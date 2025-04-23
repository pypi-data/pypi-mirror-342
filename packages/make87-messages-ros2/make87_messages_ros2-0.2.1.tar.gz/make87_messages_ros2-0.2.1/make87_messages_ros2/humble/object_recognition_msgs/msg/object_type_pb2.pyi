from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ObjectType(_message.Message):
    __slots__ = ["header", "key", "db"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    DB_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    key: str
    db: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., key: _Optional[str] = ..., db: _Optional[str] = ...) -> None: ...
