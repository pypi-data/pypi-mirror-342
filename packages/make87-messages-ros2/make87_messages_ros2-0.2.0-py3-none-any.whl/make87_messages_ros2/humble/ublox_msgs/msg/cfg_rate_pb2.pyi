from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CfgRATE(_message.Message):
    __slots__ = ["header", "meas_rate", "nav_rate", "time_ref"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MEAS_RATE_FIELD_NUMBER: _ClassVar[int]
    NAV_RATE_FIELD_NUMBER: _ClassVar[int]
    TIME_REF_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    meas_rate: int
    nav_rate: int
    time_ref: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., meas_rate: _Optional[int] = ..., nav_rate: _Optional[int] = ..., time_ref: _Optional[int] = ...) -> None: ...
