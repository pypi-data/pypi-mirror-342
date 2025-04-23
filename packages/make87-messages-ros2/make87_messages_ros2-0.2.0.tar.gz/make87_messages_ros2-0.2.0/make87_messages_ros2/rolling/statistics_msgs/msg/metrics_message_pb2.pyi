from make87_messages_ros2.rolling.builtin_interfaces.msg import time_pb2 as _time_pb2
from make87_messages_ros2.rolling.statistics_msgs.msg import statistic_data_point_pb2 as _statistic_data_point_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MetricsMessage(_message.Message):
    __slots__ = ["measurement_source_name", "metrics_source", "unit", "window_start", "window_stop", "statistics"]
    MEASUREMENT_SOURCE_NAME_FIELD_NUMBER: _ClassVar[int]
    METRICS_SOURCE_FIELD_NUMBER: _ClassVar[int]
    UNIT_FIELD_NUMBER: _ClassVar[int]
    WINDOW_START_FIELD_NUMBER: _ClassVar[int]
    WINDOW_STOP_FIELD_NUMBER: _ClassVar[int]
    STATISTICS_FIELD_NUMBER: _ClassVar[int]
    measurement_source_name: str
    metrics_source: str
    unit: str
    window_start: _time_pb2.Time
    window_stop: _time_pb2.Time
    statistics: _containers.RepeatedCompositeFieldContainer[_statistic_data_point_pb2.StatisticDataPoint]
    def __init__(self, measurement_source_name: _Optional[str] = ..., metrics_source: _Optional[str] = ..., unit: _Optional[str] = ..., window_start: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., window_stop: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., statistics: _Optional[_Iterable[_Union[_statistic_data_point_pb2.StatisticDataPoint, _Mapping]]] = ...) -> None: ...
