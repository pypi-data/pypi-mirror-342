from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Information(_message.Message):
    __slots__ = ["header", "ros2_header", "sensor_type", "hw_temperature", "sensor_blind", "sw_fail", "hw_fail", "can_fail", "config_fail", "diag_mode", "dtc", "dtc_order_id", "sensor_not_safe"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    SENSOR_TYPE_FIELD_NUMBER: _ClassVar[int]
    HW_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    SENSOR_BLIND_FIELD_NUMBER: _ClassVar[int]
    SW_FAIL_FIELD_NUMBER: _ClassVar[int]
    HW_FAIL_FIELD_NUMBER: _ClassVar[int]
    CAN_FAIL_FIELD_NUMBER: _ClassVar[int]
    CONFIG_FAIL_FIELD_NUMBER: _ClassVar[int]
    DIAG_MODE_FIELD_NUMBER: _ClassVar[int]
    DTC_FIELD_NUMBER: _ClassVar[int]
    DTC_ORDER_ID_FIELD_NUMBER: _ClassVar[int]
    SENSOR_NOT_SAFE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    sensor_type: int
    hw_temperature: float
    sensor_blind: bool
    sw_fail: bool
    hw_fail: bool
    can_fail: bool
    config_fail: bool
    diag_mode: bool
    dtc: int
    dtc_order_id: int
    sensor_not_safe: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., sensor_type: _Optional[int] = ..., hw_temperature: _Optional[float] = ..., sensor_blind: bool = ..., sw_fail: bool = ..., hw_fail: bool = ..., can_fail: bool = ..., config_fail: bool = ..., diag_mode: bool = ..., dtc: _Optional[int] = ..., dtc_order_id: _Optional[int] = ..., sensor_not_safe: bool = ...) -> None: ...
