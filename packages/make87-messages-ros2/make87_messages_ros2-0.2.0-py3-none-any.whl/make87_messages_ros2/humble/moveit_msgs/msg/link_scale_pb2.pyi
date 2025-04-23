from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LinkScale(_message.Message):
    __slots__ = ["header", "link_name", "scale"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    LINK_NAME_FIELD_NUMBER: _ClassVar[int]
    SCALE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    link_name: str
    scale: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., link_name: _Optional[str] = ..., scale: _Optional[float] = ...) -> None: ...
