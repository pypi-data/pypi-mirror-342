from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SingleBatteryInfo(_message.Message):
    __slots__ = ["header", "ros2_header", "battery_index", "voltage", "current", "full_capacity", "capacity_remain", "capacity_percentage", "temperature", "cell_count", "self_check_error", "closed_reason", "abnormal_comm", "is_embed"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    BATTERY_INDEX_FIELD_NUMBER: _ClassVar[int]
    VOLTAGE_FIELD_NUMBER: _ClassVar[int]
    CURRENT_FIELD_NUMBER: _ClassVar[int]
    FULL_CAPACITY_FIELD_NUMBER: _ClassVar[int]
    CAPACITY_REMAIN_FIELD_NUMBER: _ClassVar[int]
    CAPACITY_PERCENTAGE_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    CELL_COUNT_FIELD_NUMBER: _ClassVar[int]
    SELF_CHECK_ERROR_FIELD_NUMBER: _ClassVar[int]
    CLOSED_REASON_FIELD_NUMBER: _ClassVar[int]
    ABNORMAL_COMM_FIELD_NUMBER: _ClassVar[int]
    IS_EMBED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    battery_index: int
    voltage: float
    current: float
    full_capacity: float
    capacity_remain: float
    capacity_percentage: float
    temperature: float
    cell_count: int
    self_check_error: int
    closed_reason: int
    abnormal_comm: int
    is_embed: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., battery_index: _Optional[int] = ..., voltage: _Optional[float] = ..., current: _Optional[float] = ..., full_capacity: _Optional[float] = ..., capacity_remain: _Optional[float] = ..., capacity_percentage: _Optional[float] = ..., temperature: _Optional[float] = ..., cell_count: _Optional[int] = ..., self_check_error: _Optional[int] = ..., closed_reason: _Optional[int] = ..., abnormal_comm: _Optional[int] = ..., is_embed: _Optional[int] = ...) -> None: ...
