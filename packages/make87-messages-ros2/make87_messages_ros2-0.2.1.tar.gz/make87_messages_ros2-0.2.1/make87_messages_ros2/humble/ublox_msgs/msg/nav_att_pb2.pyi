from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NavATT(_message.Message):
    __slots__ = ["header", "i_tow", "version", "reserved0", "roll", "pitch", "heading", "acc_roll", "acc_pitch", "acc_heading"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    I_TOW_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    RESERVED0_FIELD_NUMBER: _ClassVar[int]
    ROLL_FIELD_NUMBER: _ClassVar[int]
    PITCH_FIELD_NUMBER: _ClassVar[int]
    HEADING_FIELD_NUMBER: _ClassVar[int]
    ACC_ROLL_FIELD_NUMBER: _ClassVar[int]
    ACC_PITCH_FIELD_NUMBER: _ClassVar[int]
    ACC_HEADING_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    i_tow: int
    version: int
    reserved0: _containers.RepeatedScalarFieldContainer[int]
    roll: int
    pitch: int
    heading: int
    acc_roll: int
    acc_pitch: int
    acc_heading: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., i_tow: _Optional[int] = ..., version: _Optional[int] = ..., reserved0: _Optional[_Iterable[int]] = ..., roll: _Optional[int] = ..., pitch: _Optional[int] = ..., heading: _Optional[int] = ..., acc_roll: _Optional[int] = ..., acc_pitch: _Optional[int] = ..., acc_heading: _Optional[int] = ...) -> None: ...
