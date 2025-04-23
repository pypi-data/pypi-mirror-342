from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SonarUsage(_message.Message):
    __slots__ = ["header", "left", "right"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    LEFT_FIELD_NUMBER: _ClassVar[int]
    RIGHT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    left: bool
    right: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., left: bool = ..., right: bool = ...) -> None: ...
