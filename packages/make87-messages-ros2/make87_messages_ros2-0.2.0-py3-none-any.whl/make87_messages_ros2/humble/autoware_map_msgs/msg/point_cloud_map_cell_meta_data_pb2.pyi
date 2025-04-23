from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PointCloudMapCellMetaData(_message.Message):
    __slots__ = ["header", "min_x", "min_y", "max_x", "max_y"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MIN_X_FIELD_NUMBER: _ClassVar[int]
    MIN_Y_FIELD_NUMBER: _ClassVar[int]
    MAX_X_FIELD_NUMBER: _ClassVar[int]
    MAX_Y_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    min_x: float
    min_y: float
    max_x: float
    max_y: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., min_x: _Optional[float] = ..., min_y: _Optional[float] = ..., max_x: _Optional[float] = ..., max_y: _Optional[float] = ...) -> None: ...
