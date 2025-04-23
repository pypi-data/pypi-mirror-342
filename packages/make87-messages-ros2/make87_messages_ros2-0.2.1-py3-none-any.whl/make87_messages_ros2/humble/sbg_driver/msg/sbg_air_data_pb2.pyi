from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.sbg_driver.msg import sbg_air_data_status_pb2 as _sbg_air_data_status_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SbgAirData(_message.Message):
    __slots__ = ["header", "ros2_header", "time_stamp", "status", "pressure_abs", "altitude", "pressure_diff", "true_air_speed", "air_temperature"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    TIME_STAMP_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    PRESSURE_ABS_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_FIELD_NUMBER: _ClassVar[int]
    PRESSURE_DIFF_FIELD_NUMBER: _ClassVar[int]
    TRUE_AIR_SPEED_FIELD_NUMBER: _ClassVar[int]
    AIR_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    time_stamp: int
    status: _sbg_air_data_status_pb2.SbgAirDataStatus
    pressure_abs: float
    altitude: float
    pressure_diff: float
    true_air_speed: float
    air_temperature: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., time_stamp: _Optional[int] = ..., status: _Optional[_Union[_sbg_air_data_status_pb2.SbgAirDataStatus, _Mapping]] = ..., pressure_abs: _Optional[float] = ..., altitude: _Optional[float] = ..., pressure_diff: _Optional[float] = ..., true_air_speed: _Optional[float] = ..., air_temperature: _Optional[float] = ...) -> None: ...
