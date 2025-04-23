from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ForceResistance(_message.Message):
    __slots__ = ["header", "name", "px", "py", "pz", "fx", "fy", "fz"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PX_FIELD_NUMBER: _ClassVar[int]
    PY_FIELD_NUMBER: _ClassVar[int]
    PZ_FIELD_NUMBER: _ClassVar[int]
    FX_FIELD_NUMBER: _ClassVar[int]
    FY_FIELD_NUMBER: _ClassVar[int]
    FZ_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    name: str
    px: float
    py: float
    pz: float
    fx: float
    fy: float
    fz: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., name: _Optional[str] = ..., px: _Optional[float] = ..., py: _Optional[float] = ..., pz: _Optional[float] = ..., fx: _Optional[float] = ..., fy: _Optional[float] = ..., fz: _Optional[float] = ...) -> None: ...
