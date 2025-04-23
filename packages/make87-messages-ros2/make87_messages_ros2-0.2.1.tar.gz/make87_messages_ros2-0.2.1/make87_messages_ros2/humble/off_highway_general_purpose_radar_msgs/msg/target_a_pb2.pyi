from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TargetA(_message.Message):
    __slots__ = ["header", "can_id", "stamp", "id", "radial_distance", "radial_velocity", "reflected_power", "azimuth_angle", "measured"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CAN_ID_FIELD_NUMBER: _ClassVar[int]
    STAMP_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    RADIAL_DISTANCE_FIELD_NUMBER: _ClassVar[int]
    RADIAL_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    REFLECTED_POWER_FIELD_NUMBER: _ClassVar[int]
    AZIMUTH_ANGLE_FIELD_NUMBER: _ClassVar[int]
    MEASURED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    can_id: int
    stamp: _time_pb2.Time
    id: int
    radial_distance: float
    radial_velocity: float
    reflected_power: float
    azimuth_angle: float
    measured: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., can_id: _Optional[int] = ..., stamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., id: _Optional[int] = ..., radial_distance: _Optional[float] = ..., radial_velocity: _Optional[float] = ..., reflected_power: _Optional[float] = ..., azimuth_angle: _Optional[float] = ..., measured: bool = ...) -> None: ...
