from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UBXNavDOP(_message.Message):
    __slots__ = ["header", "ros2_header", "itow", "g_dop", "p_dop", "t_dop", "v_dop", "h_dop", "n_dop", "e_dop"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    ITOW_FIELD_NUMBER: _ClassVar[int]
    G_DOP_FIELD_NUMBER: _ClassVar[int]
    P_DOP_FIELD_NUMBER: _ClassVar[int]
    T_DOP_FIELD_NUMBER: _ClassVar[int]
    V_DOP_FIELD_NUMBER: _ClassVar[int]
    H_DOP_FIELD_NUMBER: _ClassVar[int]
    N_DOP_FIELD_NUMBER: _ClassVar[int]
    E_DOP_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    itow: int
    g_dop: int
    p_dop: int
    t_dop: int
    v_dop: int
    h_dop: int
    n_dop: int
    e_dop: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., itow: _Optional[int] = ..., g_dop: _Optional[int] = ..., p_dop: _Optional[int] = ..., t_dop: _Optional[int] = ..., v_dop: _Optional[int] = ..., h_dop: _Optional[int] = ..., n_dop: _Optional[int] = ..., e_dop: _Optional[int] = ...) -> None: ...
