from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Gpgga(_message.Message):
    __slots__ = ["header", "ros2_header", "message_id", "utc_seconds", "lat", "lon", "lat_dir", "lon_dir", "gps_qual", "num_sats", "hdop", "alt", "altitude_units", "undulation", "undulation_units", "diff_age", "station_id"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_ID_FIELD_NUMBER: _ClassVar[int]
    UTC_SECONDS_FIELD_NUMBER: _ClassVar[int]
    LAT_FIELD_NUMBER: _ClassVar[int]
    LON_FIELD_NUMBER: _ClassVar[int]
    LAT_DIR_FIELD_NUMBER: _ClassVar[int]
    LON_DIR_FIELD_NUMBER: _ClassVar[int]
    GPS_QUAL_FIELD_NUMBER: _ClassVar[int]
    NUM_SATS_FIELD_NUMBER: _ClassVar[int]
    HDOP_FIELD_NUMBER: _ClassVar[int]
    ALT_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_UNITS_FIELD_NUMBER: _ClassVar[int]
    UNDULATION_FIELD_NUMBER: _ClassVar[int]
    UNDULATION_UNITS_FIELD_NUMBER: _ClassVar[int]
    DIFF_AGE_FIELD_NUMBER: _ClassVar[int]
    STATION_ID_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    message_id: str
    utc_seconds: float
    lat: float
    lon: float
    lat_dir: str
    lon_dir: str
    gps_qual: int
    num_sats: int
    hdop: float
    alt: float
    altitude_units: str
    undulation: float
    undulation_units: str
    diff_age: int
    station_id: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., message_id: _Optional[str] = ..., utc_seconds: _Optional[float] = ..., lat: _Optional[float] = ..., lon: _Optional[float] = ..., lat_dir: _Optional[str] = ..., lon_dir: _Optional[str] = ..., gps_qual: _Optional[int] = ..., num_sats: _Optional[int] = ..., hdop: _Optional[float] = ..., alt: _Optional[float] = ..., altitude_units: _Optional[str] = ..., undulation: _Optional[float] = ..., undulation_units: _Optional[str] = ..., diff_age: _Optional[int] = ..., station_id: _Optional[str] = ...) -> None: ...
