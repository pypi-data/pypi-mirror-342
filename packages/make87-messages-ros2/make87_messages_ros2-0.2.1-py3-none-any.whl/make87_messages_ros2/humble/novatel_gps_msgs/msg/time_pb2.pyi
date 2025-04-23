from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Time(_message.Message):
    __slots__ = ["header", "ros2_header", "clock_status", "offset", "offset_std", "utc_offset", "utc_year", "utc_month", "utc_day", "utc_hour", "utc_minute", "utc_millisecond", "utc_status"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    CLOCK_STATUS_FIELD_NUMBER: _ClassVar[int]
    OFFSET_FIELD_NUMBER: _ClassVar[int]
    OFFSET_STD_FIELD_NUMBER: _ClassVar[int]
    UTC_OFFSET_FIELD_NUMBER: _ClassVar[int]
    UTC_YEAR_FIELD_NUMBER: _ClassVar[int]
    UTC_MONTH_FIELD_NUMBER: _ClassVar[int]
    UTC_DAY_FIELD_NUMBER: _ClassVar[int]
    UTC_HOUR_FIELD_NUMBER: _ClassVar[int]
    UTC_MINUTE_FIELD_NUMBER: _ClassVar[int]
    UTC_MILLISECOND_FIELD_NUMBER: _ClassVar[int]
    UTC_STATUS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    clock_status: str
    offset: float
    offset_std: float
    utc_offset: float
    utc_year: int
    utc_month: int
    utc_day: int
    utc_hour: int
    utc_minute: int
    utc_millisecond: int
    utc_status: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., clock_status: _Optional[str] = ..., offset: _Optional[float] = ..., offset_std: _Optional[float] = ..., utc_offset: _Optional[float] = ..., utc_year: _Optional[int] = ..., utc_month: _Optional[int] = ..., utc_day: _Optional[int] = ..., utc_hour: _Optional[int] = ..., utc_minute: _Optional[int] = ..., utc_millisecond: _Optional[int] = ..., utc_status: _Optional[str] = ...) -> None: ...
