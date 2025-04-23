from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RobotConfig(_message.Message):
    __slots__ = ["header", "body_id", "body_version", "head_id", "head_version"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BODY_ID_FIELD_NUMBER: _ClassVar[int]
    BODY_VERSION_FIELD_NUMBER: _ClassVar[int]
    HEAD_ID_FIELD_NUMBER: _ClassVar[int]
    HEAD_VERSION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    body_id: str
    body_version: str
    head_id: str
    head_version: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., body_id: _Optional[str] = ..., body_version: _Optional[str] = ..., head_id: _Optional[str] = ..., head_version: _Optional[str] = ...) -> None: ...
