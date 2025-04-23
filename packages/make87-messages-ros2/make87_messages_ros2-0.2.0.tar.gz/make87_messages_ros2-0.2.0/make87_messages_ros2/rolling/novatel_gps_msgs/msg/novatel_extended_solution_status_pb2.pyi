from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class NovatelExtendedSolutionStatus(_message.Message):
    __slots__ = ["original_mask", "advance_rtk_verified", "psuedorange_iono_correction"]
    ORIGINAL_MASK_FIELD_NUMBER: _ClassVar[int]
    ADVANCE_RTK_VERIFIED_FIELD_NUMBER: _ClassVar[int]
    PSUEDORANGE_IONO_CORRECTION_FIELD_NUMBER: _ClassVar[int]
    original_mask: int
    advance_rtk_verified: bool
    psuedorange_iono_correction: str
    def __init__(self, original_mask: _Optional[int] = ..., advance_rtk_verified: bool = ..., psuedorange_iono_correction: _Optional[str] = ...) -> None: ...
