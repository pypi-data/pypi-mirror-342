from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GetWorldPropertiesRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetWorldPropertiesResponse(_message.Message):
    __slots__ = ["sim_time", "model_names", "rendering_enabled", "success", "status_message"]
    SIM_TIME_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAMES_FIELD_NUMBER: _ClassVar[int]
    RENDERING_ENABLED_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    sim_time: float
    model_names: _containers.RepeatedScalarFieldContainer[str]
    rendering_enabled: bool
    success: bool
    status_message: str
    def __init__(self, sim_time: _Optional[float] = ..., model_names: _Optional[_Iterable[str]] = ..., rendering_enabled: bool = ..., success: bool = ..., status_message: _Optional[str] = ...) -> None: ...
