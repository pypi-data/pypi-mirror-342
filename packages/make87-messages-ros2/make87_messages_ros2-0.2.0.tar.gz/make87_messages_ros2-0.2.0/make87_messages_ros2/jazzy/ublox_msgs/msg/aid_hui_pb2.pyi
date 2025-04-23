from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AidHUI(_message.Message):
    __slots__ = ["health", "utc_a0", "utc_a1", "utc_tow", "utc_wnt", "utc_ls", "utc_wnf", "utc_dn", "utc_lsf", "utc_spare", "klob_a0", "klob_a1", "klob_a2", "klob_a3", "klob_b0", "klob_b1", "klob_b2", "klob_b3", "flags"]
    HEALTH_FIELD_NUMBER: _ClassVar[int]
    UTC_A0_FIELD_NUMBER: _ClassVar[int]
    UTC_A1_FIELD_NUMBER: _ClassVar[int]
    UTC_TOW_FIELD_NUMBER: _ClassVar[int]
    UTC_WNT_FIELD_NUMBER: _ClassVar[int]
    UTC_LS_FIELD_NUMBER: _ClassVar[int]
    UTC_WNF_FIELD_NUMBER: _ClassVar[int]
    UTC_DN_FIELD_NUMBER: _ClassVar[int]
    UTC_LSF_FIELD_NUMBER: _ClassVar[int]
    UTC_SPARE_FIELD_NUMBER: _ClassVar[int]
    KLOB_A0_FIELD_NUMBER: _ClassVar[int]
    KLOB_A1_FIELD_NUMBER: _ClassVar[int]
    KLOB_A2_FIELD_NUMBER: _ClassVar[int]
    KLOB_A3_FIELD_NUMBER: _ClassVar[int]
    KLOB_B0_FIELD_NUMBER: _ClassVar[int]
    KLOB_B1_FIELD_NUMBER: _ClassVar[int]
    KLOB_B2_FIELD_NUMBER: _ClassVar[int]
    KLOB_B3_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    health: int
    utc_a0: float
    utc_a1: float
    utc_tow: int
    utc_wnt: int
    utc_ls: int
    utc_wnf: int
    utc_dn: int
    utc_lsf: int
    utc_spare: int
    klob_a0: float
    klob_a1: float
    klob_a2: float
    klob_a3: float
    klob_b0: float
    klob_b1: float
    klob_b2: float
    klob_b3: float
    flags: int
    def __init__(self, health: _Optional[int] = ..., utc_a0: _Optional[float] = ..., utc_a1: _Optional[float] = ..., utc_tow: _Optional[int] = ..., utc_wnt: _Optional[int] = ..., utc_ls: _Optional[int] = ..., utc_wnf: _Optional[int] = ..., utc_dn: _Optional[int] = ..., utc_lsf: _Optional[int] = ..., utc_spare: _Optional[int] = ..., klob_a0: _Optional[float] = ..., klob_a1: _Optional[float] = ..., klob_a2: _Optional[float] = ..., klob_a3: _Optional[float] = ..., klob_b0: _Optional[float] = ..., klob_b1: _Optional[float] = ..., klob_b2: _Optional[float] = ..., klob_b3: _Optional[float] = ..., flags: _Optional[int] = ...) -> None: ...
