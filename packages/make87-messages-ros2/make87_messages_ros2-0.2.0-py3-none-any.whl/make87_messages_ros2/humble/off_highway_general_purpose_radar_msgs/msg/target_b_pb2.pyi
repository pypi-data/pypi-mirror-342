from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TargetB(_message.Message):
    __slots__ = ["header", "can_id", "stamp", "id", "azimuth_angle_std", "radial_velocity_std", "radial_distance_std", "exist_probability", "time_since_meas"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CAN_ID_FIELD_NUMBER: _ClassVar[int]
    STAMP_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    AZIMUTH_ANGLE_STD_FIELD_NUMBER: _ClassVar[int]
    RADIAL_VELOCITY_STD_FIELD_NUMBER: _ClassVar[int]
    RADIAL_DISTANCE_STD_FIELD_NUMBER: _ClassVar[int]
    EXIST_PROBABILITY_FIELD_NUMBER: _ClassVar[int]
    TIME_SINCE_MEAS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    can_id: int
    stamp: _time_pb2.Time
    id: int
    azimuth_angle_std: float
    radial_velocity_std: float
    radial_distance_std: float
    exist_probability: float
    time_since_meas: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., can_id: _Optional[int] = ..., stamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., id: _Optional[int] = ..., azimuth_angle_std: _Optional[float] = ..., radial_velocity_std: _Optional[float] = ..., radial_distance_std: _Optional[float] = ..., exist_probability: _Optional[float] = ..., time_since_meas: _Optional[float] = ...) -> None: ...
