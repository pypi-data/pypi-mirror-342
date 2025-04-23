from make87_messages_ros2.jazzy.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Statistics(_message.Message):
    __slots__ = ["count", "stamp", "tick_duration", "tick_duration_average", "tick_duration_variance", "tick_interval", "tick_interval_average", "tick_interval_variance"]
    COUNT_FIELD_NUMBER: _ClassVar[int]
    STAMP_FIELD_NUMBER: _ClassVar[int]
    TICK_DURATION_FIELD_NUMBER: _ClassVar[int]
    TICK_DURATION_AVERAGE_FIELD_NUMBER: _ClassVar[int]
    TICK_DURATION_VARIANCE_FIELD_NUMBER: _ClassVar[int]
    TICK_INTERVAL_FIELD_NUMBER: _ClassVar[int]
    TICK_INTERVAL_AVERAGE_FIELD_NUMBER: _ClassVar[int]
    TICK_INTERVAL_VARIANCE_FIELD_NUMBER: _ClassVar[int]
    count: int
    stamp: _time_pb2.Time
    tick_duration: float
    tick_duration_average: float
    tick_duration_variance: float
    tick_interval: float
    tick_interval_average: float
    tick_interval_variance: float
    def __init__(self, count: _Optional[int] = ..., stamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., tick_duration: _Optional[float] = ..., tick_duration_average: _Optional[float] = ..., tick_duration_variance: _Optional[float] = ..., tick_interval: _Optional[float] = ..., tick_interval_average: _Optional[float] = ..., tick_interval_variance: _Optional[float] = ...) -> None: ...
