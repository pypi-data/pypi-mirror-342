from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NavDOP(_message.Message):
    __slots__ = ["header", "i_tow", "g_dop", "p_dop", "t_dop", "v_dop", "h_dop", "n_dop", "e_dop"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    I_TOW_FIELD_NUMBER: _ClassVar[int]
    G_DOP_FIELD_NUMBER: _ClassVar[int]
    P_DOP_FIELD_NUMBER: _ClassVar[int]
    T_DOP_FIELD_NUMBER: _ClassVar[int]
    V_DOP_FIELD_NUMBER: _ClassVar[int]
    H_DOP_FIELD_NUMBER: _ClassVar[int]
    N_DOP_FIELD_NUMBER: _ClassVar[int]
    E_DOP_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    i_tow: int
    g_dop: int
    p_dop: int
    t_dop: int
    v_dop: int
    h_dop: int
    n_dop: int
    e_dop: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., i_tow: _Optional[int] = ..., g_dop: _Optional[int] = ..., p_dop: _Optional[int] = ..., t_dop: _Optional[int] = ..., v_dop: _Optional[int] = ..., h_dop: _Optional[int] = ..., n_dop: _Optional[int] = ..., e_dop: _Optional[int] = ...) -> None: ...
