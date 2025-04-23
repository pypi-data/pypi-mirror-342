from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RxmRAWXMeas(_message.Message):
    __slots__ = ["pr_mes", "cp_mes", "do_mes", "gnss_id", "sv_id", "reserved0", "freq_id", "locktime", "cno", "pr_stdev", "cp_stdev", "do_stdev", "trk_stat", "reserved1"]
    PR_MES_FIELD_NUMBER: _ClassVar[int]
    CP_MES_FIELD_NUMBER: _ClassVar[int]
    DO_MES_FIELD_NUMBER: _ClassVar[int]
    GNSS_ID_FIELD_NUMBER: _ClassVar[int]
    SV_ID_FIELD_NUMBER: _ClassVar[int]
    RESERVED0_FIELD_NUMBER: _ClassVar[int]
    FREQ_ID_FIELD_NUMBER: _ClassVar[int]
    LOCKTIME_FIELD_NUMBER: _ClassVar[int]
    CNO_FIELD_NUMBER: _ClassVar[int]
    PR_STDEV_FIELD_NUMBER: _ClassVar[int]
    CP_STDEV_FIELD_NUMBER: _ClassVar[int]
    DO_STDEV_FIELD_NUMBER: _ClassVar[int]
    TRK_STAT_FIELD_NUMBER: _ClassVar[int]
    RESERVED1_FIELD_NUMBER: _ClassVar[int]
    pr_mes: float
    cp_mes: float
    do_mes: float
    gnss_id: int
    sv_id: int
    reserved0: int
    freq_id: int
    locktime: int
    cno: int
    pr_stdev: int
    cp_stdev: int
    do_stdev: int
    trk_stat: int
    reserved1: int
    def __init__(self, pr_mes: _Optional[float] = ..., cp_mes: _Optional[float] = ..., do_mes: _Optional[float] = ..., gnss_id: _Optional[int] = ..., sv_id: _Optional[int] = ..., reserved0: _Optional[int] = ..., freq_id: _Optional[int] = ..., locktime: _Optional[int] = ..., cno: _Optional[int] = ..., pr_stdev: _Optional[int] = ..., cp_stdev: _Optional[int] = ..., do_stdev: _Optional[int] = ..., trk_stat: _Optional[int] = ..., reserved1: _Optional[int] = ...) -> None: ...
