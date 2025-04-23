from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CameraSetFocusTargetRequest(_message.Message):
    __slots__ = ["header", "payload_index", "x_target", "y_target"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_INDEX_FIELD_NUMBER: _ClassVar[int]
    X_TARGET_FIELD_NUMBER: _ClassVar[int]
    Y_TARGET_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    payload_index: int
    x_target: float
    y_target: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., payload_index: _Optional[int] = ..., x_target: _Optional[float] = ..., y_target: _Optional[float] = ...) -> None: ...

class CameraSetFocusTargetResponse(_message.Message):
    __slots__ = ["header", "success"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ...) -> None: ...
