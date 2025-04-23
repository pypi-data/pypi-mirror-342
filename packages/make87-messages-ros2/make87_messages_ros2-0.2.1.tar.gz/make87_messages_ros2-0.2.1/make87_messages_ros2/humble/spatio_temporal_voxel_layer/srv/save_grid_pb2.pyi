from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SaveGridRequest(_message.Message):
    __slots__ = ["header", "file_name"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FILE_NAME_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    file_name: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., file_name: _Optional[str] = ...) -> None: ...

class SaveGridResponse(_message.Message):
    __slots__ = ["header", "map_size_bytes", "status"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MAP_SIZE_BYTES_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    map_size_bytes: float
    status: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., map_size_bytes: _Optional[float] = ..., status: bool = ...) -> None: ...
