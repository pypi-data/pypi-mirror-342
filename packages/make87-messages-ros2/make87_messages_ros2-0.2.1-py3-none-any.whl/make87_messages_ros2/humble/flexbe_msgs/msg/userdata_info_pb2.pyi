from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UserdataInfo(_message.Message):
    __slots__ = ["header", "state", "key", "type", "data"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    state: str
    key: str
    type: str
    data: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., state: _Optional[str] = ..., key: _Optional[str] = ..., type: _Optional[str] = ..., data: _Optional[str] = ...) -> None: ...
