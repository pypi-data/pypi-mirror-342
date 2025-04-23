from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NovatelExtendedSolutionStatus(_message.Message):
    __slots__ = ["header", "original_mask", "advance_rtk_verified", "psuedorange_iono_correction"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_MASK_FIELD_NUMBER: _ClassVar[int]
    ADVANCE_RTK_VERIFIED_FIELD_NUMBER: _ClassVar[int]
    PSUEDORANGE_IONO_CORRECTION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    original_mask: int
    advance_rtk_verified: bool
    psuedorange_iono_correction: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., original_mask: _Optional[int] = ..., advance_rtk_verified: bool = ..., psuedorange_iono_correction: _Optional[str] = ...) -> None: ...
