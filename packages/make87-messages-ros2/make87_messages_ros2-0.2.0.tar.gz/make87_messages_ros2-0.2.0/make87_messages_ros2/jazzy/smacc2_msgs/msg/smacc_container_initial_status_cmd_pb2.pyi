from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SmaccContainerInitialStatusCmd(_message.Message):
    __slots__ = ["path", "initial_states", "local_data"]
    PATH_FIELD_NUMBER: _ClassVar[int]
    INITIAL_STATES_FIELD_NUMBER: _ClassVar[int]
    LOCAL_DATA_FIELD_NUMBER: _ClassVar[int]
    path: str
    initial_states: _containers.RepeatedScalarFieldContainer[str]
    local_data: str
    def __init__(self, path: _Optional[str] = ..., initial_states: _Optional[_Iterable[str]] = ..., local_data: _Optional[str] = ...) -> None: ...
