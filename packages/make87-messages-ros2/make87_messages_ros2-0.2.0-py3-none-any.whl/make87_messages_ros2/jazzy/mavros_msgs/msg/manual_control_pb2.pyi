from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ManualControl(_message.Message):
    __slots__ = ["header", "x", "y", "z", "r", "buttons", "buttons2", "enabled_extensions", "s", "t", "aux1", "aux2", "aux3", "aux4", "aux5", "aux6"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    R_FIELD_NUMBER: _ClassVar[int]
    BUTTONS_FIELD_NUMBER: _ClassVar[int]
    BUTTONS2_FIELD_NUMBER: _ClassVar[int]
    ENABLED_EXTENSIONS_FIELD_NUMBER: _ClassVar[int]
    S_FIELD_NUMBER: _ClassVar[int]
    T_FIELD_NUMBER: _ClassVar[int]
    AUX1_FIELD_NUMBER: _ClassVar[int]
    AUX2_FIELD_NUMBER: _ClassVar[int]
    AUX3_FIELD_NUMBER: _ClassVar[int]
    AUX4_FIELD_NUMBER: _ClassVar[int]
    AUX5_FIELD_NUMBER: _ClassVar[int]
    AUX6_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    x: float
    y: float
    z: float
    r: float
    buttons: int
    buttons2: int
    enabled_extensions: int
    s: float
    t: float
    aux1: float
    aux2: float
    aux3: float
    aux4: float
    aux5: float
    aux6: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., x: _Optional[float] = ..., y: _Optional[float] = ..., z: _Optional[float] = ..., r: _Optional[float] = ..., buttons: _Optional[int] = ..., buttons2: _Optional[int] = ..., enabled_extensions: _Optional[int] = ..., s: _Optional[float] = ..., t: _Optional[float] = ..., aux1: _Optional[float] = ..., aux2: _Optional[float] = ..., aux3: _Optional[float] = ..., aux4: _Optional[float] = ..., aux5: _Optional[float] = ..., aux6: _Optional[float] = ...) -> None: ...
