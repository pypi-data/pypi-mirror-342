from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.gps_msgs.msg import gps_status_pb2 as _gps_status_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GPSFix(_message.Message):
    __slots__ = ["header", "ros2_header", "status", "latitude", "longitude", "altitude", "track", "speed", "climb", "pitch", "roll", "dip", "time", "gdop", "pdop", "hdop", "vdop", "tdop", "err", "err_horz", "err_vert", "err_track", "err_speed", "err_climb", "err_time", "err_pitch", "err_roll", "err_dip", "position_covariance", "position_covariance_type"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_FIELD_NUMBER: _ClassVar[int]
    TRACK_FIELD_NUMBER: _ClassVar[int]
    SPEED_FIELD_NUMBER: _ClassVar[int]
    CLIMB_FIELD_NUMBER: _ClassVar[int]
    PITCH_FIELD_NUMBER: _ClassVar[int]
    ROLL_FIELD_NUMBER: _ClassVar[int]
    DIP_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    GDOP_FIELD_NUMBER: _ClassVar[int]
    PDOP_FIELD_NUMBER: _ClassVar[int]
    HDOP_FIELD_NUMBER: _ClassVar[int]
    VDOP_FIELD_NUMBER: _ClassVar[int]
    TDOP_FIELD_NUMBER: _ClassVar[int]
    ERR_FIELD_NUMBER: _ClassVar[int]
    ERR_HORZ_FIELD_NUMBER: _ClassVar[int]
    ERR_VERT_FIELD_NUMBER: _ClassVar[int]
    ERR_TRACK_FIELD_NUMBER: _ClassVar[int]
    ERR_SPEED_FIELD_NUMBER: _ClassVar[int]
    ERR_CLIMB_FIELD_NUMBER: _ClassVar[int]
    ERR_TIME_FIELD_NUMBER: _ClassVar[int]
    ERR_PITCH_FIELD_NUMBER: _ClassVar[int]
    ERR_ROLL_FIELD_NUMBER: _ClassVar[int]
    ERR_DIP_FIELD_NUMBER: _ClassVar[int]
    POSITION_COVARIANCE_FIELD_NUMBER: _ClassVar[int]
    POSITION_COVARIANCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    status: _gps_status_pb2.GPSStatus
    latitude: float
    longitude: float
    altitude: float
    track: float
    speed: float
    climb: float
    pitch: float
    roll: float
    dip: float
    time: float
    gdop: float
    pdop: float
    hdop: float
    vdop: float
    tdop: float
    err: float
    err_horz: float
    err_vert: float
    err_track: float
    err_speed: float
    err_climb: float
    err_time: float
    err_pitch: float
    err_roll: float
    err_dip: float
    position_covariance: _containers.RepeatedScalarFieldContainer[float]
    position_covariance_type: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., status: _Optional[_Union[_gps_status_pb2.GPSStatus, _Mapping]] = ..., latitude: _Optional[float] = ..., longitude: _Optional[float] = ..., altitude: _Optional[float] = ..., track: _Optional[float] = ..., speed: _Optional[float] = ..., climb: _Optional[float] = ..., pitch: _Optional[float] = ..., roll: _Optional[float] = ..., dip: _Optional[float] = ..., time: _Optional[float] = ..., gdop: _Optional[float] = ..., pdop: _Optional[float] = ..., hdop: _Optional[float] = ..., vdop: _Optional[float] = ..., tdop: _Optional[float] = ..., err: _Optional[float] = ..., err_horz: _Optional[float] = ..., err_vert: _Optional[float] = ..., err_track: _Optional[float] = ..., err_speed: _Optional[float] = ..., err_climb: _Optional[float] = ..., err_time: _Optional[float] = ..., err_pitch: _Optional[float] = ..., err_roll: _Optional[float] = ..., err_dip: _Optional[float] = ..., position_covariance: _Optional[_Iterable[float]] = ..., position_covariance_type: _Optional[int] = ...) -> None: ...
