from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ItineraryReached(_message.Message):
    __slots__ = ["header", "participant", "plan", "reached_checkpoints", "progress_version"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PARTICIPANT_FIELD_NUMBER: _ClassVar[int]
    PLAN_FIELD_NUMBER: _ClassVar[int]
    REACHED_CHECKPOINTS_FIELD_NUMBER: _ClassVar[int]
    PROGRESS_VERSION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    participant: int
    plan: int
    reached_checkpoints: _containers.RepeatedScalarFieldContainer[int]
    progress_version: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., participant: _Optional[int] = ..., plan: _Optional[int] = ..., reached_checkpoints: _Optional[_Iterable[int]] = ..., progress_version: _Optional[int] = ...) -> None: ...
