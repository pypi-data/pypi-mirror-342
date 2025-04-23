from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class NavTIMEUTC(_message.Message):
    __slots__ = ["i_tow", "t_acc", "nano", "year", "month", "day", "hour", "min", "sec", "valid"]
    I_TOW_FIELD_NUMBER: _ClassVar[int]
    T_ACC_FIELD_NUMBER: _ClassVar[int]
    NANO_FIELD_NUMBER: _ClassVar[int]
    YEAR_FIELD_NUMBER: _ClassVar[int]
    MONTH_FIELD_NUMBER: _ClassVar[int]
    DAY_FIELD_NUMBER: _ClassVar[int]
    HOUR_FIELD_NUMBER: _ClassVar[int]
    MIN_FIELD_NUMBER: _ClassVar[int]
    SEC_FIELD_NUMBER: _ClassVar[int]
    VALID_FIELD_NUMBER: _ClassVar[int]
    i_tow: int
    t_acc: int
    nano: int
    year: int
    month: int
    day: int
    hour: int
    min: int
    sec: int
    valid: int
    def __init__(self, i_tow: _Optional[int] = ..., t_acc: _Optional[int] = ..., nano: _Optional[int] = ..., year: _Optional[int] = ..., month: _Optional[int] = ..., day: _Optional[int] = ..., hour: _Optional[int] = ..., min: _Optional[int] = ..., sec: _Optional[int] = ..., valid: _Optional[int] = ...) -> None: ...
