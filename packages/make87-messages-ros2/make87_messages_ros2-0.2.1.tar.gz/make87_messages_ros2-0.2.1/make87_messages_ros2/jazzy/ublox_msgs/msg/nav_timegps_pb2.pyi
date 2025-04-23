from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class NavTIMEGPS(_message.Message):
    __slots__ = ["i_tow", "f_tow", "week", "leap_s", "valid", "t_acc"]
    I_TOW_FIELD_NUMBER: _ClassVar[int]
    F_TOW_FIELD_NUMBER: _ClassVar[int]
    WEEK_FIELD_NUMBER: _ClassVar[int]
    LEAP_S_FIELD_NUMBER: _ClassVar[int]
    VALID_FIELD_NUMBER: _ClassVar[int]
    T_ACC_FIELD_NUMBER: _ClassVar[int]
    i_tow: int
    f_tow: int
    week: int
    leap_s: int
    valid: int
    t_acc: int
    def __init__(self, i_tow: _Optional[int] = ..., f_tow: _Optional[int] = ..., week: _Optional[int] = ..., leap_s: _Optional[int] = ..., valid: _Optional[int] = ..., t_acc: _Optional[int] = ...) -> None: ...
