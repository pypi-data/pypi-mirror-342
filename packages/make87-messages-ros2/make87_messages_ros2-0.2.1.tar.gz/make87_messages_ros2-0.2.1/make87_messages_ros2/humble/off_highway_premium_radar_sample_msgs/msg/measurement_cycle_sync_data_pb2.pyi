from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MeasurementCycleSyncData(_message.Message):
    __slots__ = ["header", "sync", "sensor_time_offset"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SYNC_FIELD_NUMBER: _ClassVar[int]
    SENSOR_TIME_OFFSET_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    sync: bool
    sensor_time_offset: _time_pb2.Time
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., sync: bool = ..., sensor_time_offset: _Optional[_Union[_time_pb2.Time, _Mapping]] = ...) -> None: ...
