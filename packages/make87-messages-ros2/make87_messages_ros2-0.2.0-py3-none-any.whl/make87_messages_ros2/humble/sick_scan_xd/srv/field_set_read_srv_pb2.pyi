from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FieldSetReadSrvRequest(_message.Message):
    __slots__ = ["header"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...

class FieldSetReadSrvResponse(_message.Message):
    __slots__ = ["header", "field_set_selection_method", "active_field_set", "success"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FIELD_SET_SELECTION_METHOD_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_SET_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    field_set_selection_method: int
    active_field_set: int
    success: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., field_set_selection_method: _Optional[int] = ..., active_field_set: _Optional[int] = ..., success: bool = ...) -> None: ...
