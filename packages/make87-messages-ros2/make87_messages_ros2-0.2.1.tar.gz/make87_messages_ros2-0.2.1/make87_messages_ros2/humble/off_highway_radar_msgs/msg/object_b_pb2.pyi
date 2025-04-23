from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ObjectB(_message.Message):
    __slots__ = ["header", "can_id", "stamp", "id", "time_since_meas", "zone", "rcs", "moving", "near", "exist_probability"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CAN_ID_FIELD_NUMBER: _ClassVar[int]
    STAMP_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    TIME_SINCE_MEAS_FIELD_NUMBER: _ClassVar[int]
    ZONE_FIELD_NUMBER: _ClassVar[int]
    RCS_FIELD_NUMBER: _ClassVar[int]
    MOVING_FIELD_NUMBER: _ClassVar[int]
    NEAR_FIELD_NUMBER: _ClassVar[int]
    EXIST_PROBABILITY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    can_id: int
    stamp: _time_pb2.Time
    id: int
    time_since_meas: float
    zone: int
    rcs: float
    moving: bool
    near: bool
    exist_probability: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., can_id: _Optional[int] = ..., stamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., id: _Optional[int] = ..., time_since_meas: _Optional[float] = ..., zone: _Optional[int] = ..., rcs: _Optional[float] = ..., moving: bool = ..., near: bool = ..., exist_probability: _Optional[float] = ...) -> None: ...
