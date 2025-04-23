from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FeatureFlags(_message.Message):
    __slots__ = ["header", "flag_none", "flag_read", "flag_write", "flag_volatile", "flag_modify_write"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FLAG_NONE_FIELD_NUMBER: _ClassVar[int]
    FLAG_READ_FIELD_NUMBER: _ClassVar[int]
    FLAG_WRITE_FIELD_NUMBER: _ClassVar[int]
    FLAG_VOLATILE_FIELD_NUMBER: _ClassVar[int]
    FLAG_MODIFY_WRITE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    flag_none: bool
    flag_read: bool
    flag_write: bool
    flag_volatile: bool
    flag_modify_write: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., flag_none: bool = ..., flag_read: bool = ..., flag_write: bool = ..., flag_volatile: bool = ..., flag_modify_write: bool = ...) -> None: ...
