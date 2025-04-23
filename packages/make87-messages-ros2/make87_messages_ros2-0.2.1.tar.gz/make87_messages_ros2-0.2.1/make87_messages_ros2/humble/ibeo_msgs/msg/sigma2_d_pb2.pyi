from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Sigma2D(_message.Message):
    __slots__ = ["header", "sigma_x", "sigma_y"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SIGMA_X_FIELD_NUMBER: _ClassVar[int]
    SIGMA_Y_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    sigma_x: int
    sigma_y: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., sigma_x: _Optional[int] = ..., sigma_y: _Optional[int] = ...) -> None: ...
