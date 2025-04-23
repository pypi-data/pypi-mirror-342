from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class TimTM2(_message.Message):
    __slots__ = ["ch", "flags", "rising_edge_count", "wn_r", "wn_f", "tow_ms_r", "tow_sub_ms_r", "tow_ms_f", "tow_sub_ms_f", "acc_est"]
    CH_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    RISING_EDGE_COUNT_FIELD_NUMBER: _ClassVar[int]
    WN_R_FIELD_NUMBER: _ClassVar[int]
    WN_F_FIELD_NUMBER: _ClassVar[int]
    TOW_MS_R_FIELD_NUMBER: _ClassVar[int]
    TOW_SUB_MS_R_FIELD_NUMBER: _ClassVar[int]
    TOW_MS_F_FIELD_NUMBER: _ClassVar[int]
    TOW_SUB_MS_F_FIELD_NUMBER: _ClassVar[int]
    ACC_EST_FIELD_NUMBER: _ClassVar[int]
    ch: int
    flags: int
    rising_edge_count: int
    wn_r: int
    wn_f: int
    tow_ms_r: int
    tow_sub_ms_r: int
    tow_ms_f: int
    tow_sub_ms_f: int
    acc_est: int
    def __init__(self, ch: _Optional[int] = ..., flags: _Optional[int] = ..., rising_edge_count: _Optional[int] = ..., wn_r: _Optional[int] = ..., wn_f: _Optional[int] = ..., tow_ms_r: _Optional[int] = ..., tow_sub_ms_r: _Optional[int] = ..., tow_ms_f: _Optional[int] = ..., tow_sub_ms_f: _Optional[int] = ..., acc_est: _Optional[int] = ...) -> None: ...
