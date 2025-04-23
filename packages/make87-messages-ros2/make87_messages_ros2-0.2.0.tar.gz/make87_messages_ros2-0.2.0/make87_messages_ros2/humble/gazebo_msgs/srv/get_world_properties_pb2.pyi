from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetWorldPropertiesRequest(_message.Message):
    __slots__ = ["header"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ...) -> None: ...

class GetWorldPropertiesResponse(_message.Message):
    __slots__ = ["header", "sim_time", "model_names", "rendering_enabled", "success", "status_message"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SIM_TIME_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAMES_FIELD_NUMBER: _ClassVar[int]
    RENDERING_ENABLED_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    sim_time: float
    model_names: _containers.RepeatedScalarFieldContainer[str]
    rendering_enabled: bool
    success: bool
    status_message: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., sim_time: _Optional[float] = ..., model_names: _Optional[_Iterable[str]] = ..., rendering_enabled: bool = ..., success: bool = ..., status_message: _Optional[str] = ...) -> None: ...
