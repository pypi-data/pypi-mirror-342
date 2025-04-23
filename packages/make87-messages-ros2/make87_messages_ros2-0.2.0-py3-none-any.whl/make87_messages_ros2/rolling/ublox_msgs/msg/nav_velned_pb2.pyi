from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class NavVELNED(_message.Message):
    __slots__ = ["i_tow", "vel_n", "vel_e", "vel_d", "speed", "g_speed", "heading", "s_acc", "c_acc"]
    I_TOW_FIELD_NUMBER: _ClassVar[int]
    VEL_N_FIELD_NUMBER: _ClassVar[int]
    VEL_E_FIELD_NUMBER: _ClassVar[int]
    VEL_D_FIELD_NUMBER: _ClassVar[int]
    SPEED_FIELD_NUMBER: _ClassVar[int]
    G_SPEED_FIELD_NUMBER: _ClassVar[int]
    HEADING_FIELD_NUMBER: _ClassVar[int]
    S_ACC_FIELD_NUMBER: _ClassVar[int]
    C_ACC_FIELD_NUMBER: _ClassVar[int]
    i_tow: int
    vel_n: int
    vel_e: int
    vel_d: int
    speed: int
    g_speed: int
    heading: int
    s_acc: int
    c_acc: int
    def __init__(self, i_tow: _Optional[int] = ..., vel_n: _Optional[int] = ..., vel_e: _Optional[int] = ..., vel_d: _Optional[int] = ..., speed: _Optional[int] = ..., g_speed: _Optional[int] = ..., heading: _Optional[int] = ..., s_acc: _Optional[int] = ..., c_acc: _Optional[int] = ...) -> None: ...
