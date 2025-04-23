from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Field(_message.Message):
    __slots__ = ["header", "ranges", "start_angle", "angular_resolution", "protective_field"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    RANGES_FIELD_NUMBER: _ClassVar[int]
    START_ANGLE_FIELD_NUMBER: _ClassVar[int]
    ANGULAR_RESOLUTION_FIELD_NUMBER: _ClassVar[int]
    PROTECTIVE_FIELD_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ranges: _containers.RepeatedScalarFieldContainer[float]
    start_angle: float
    angular_resolution: float
    protective_field: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ranges: _Optional[_Iterable[float]] = ..., start_angle: _Optional[float] = ..., angular_resolution: _Optional[float] = ..., protective_field: bool = ...) -> None: ...
