from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import duration_pb2 as _duration_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Status(_message.Message):
    __slots__ = ["header", "ros2_header", "hardware_id", "firmware_version", "mcu_uptime", "connection_uptime", "pcb_temperature", "mcu_temperature"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    HARDWARE_ID_FIELD_NUMBER: _ClassVar[int]
    FIRMWARE_VERSION_FIELD_NUMBER: _ClassVar[int]
    MCU_UPTIME_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_UPTIME_FIELD_NUMBER: _ClassVar[int]
    PCB_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    MCU_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    hardware_id: str
    firmware_version: str
    mcu_uptime: _duration_pb2.Duration
    connection_uptime: _duration_pb2.Duration
    pcb_temperature: float
    mcu_temperature: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., hardware_id: _Optional[str] = ..., firmware_version: _Optional[str] = ..., mcu_uptime: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., connection_uptime: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., pcb_temperature: _Optional[float] = ..., mcu_temperature: _Optional[float] = ...) -> None: ...
