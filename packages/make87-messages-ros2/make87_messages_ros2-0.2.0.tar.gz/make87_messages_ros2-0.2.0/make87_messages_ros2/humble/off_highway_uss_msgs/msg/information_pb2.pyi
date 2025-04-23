from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Information(_message.Message):
    __slots__ = ["header", "ros2_header", "number_sensors", "sending_pattern", "operating_mode", "outside_temperature", "sensor_blindness", "sensitivity", "sensor_faulted", "failure_status"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    NUMBER_SENSORS_FIELD_NUMBER: _ClassVar[int]
    SENDING_PATTERN_FIELD_NUMBER: _ClassVar[int]
    OPERATING_MODE_FIELD_NUMBER: _ClassVar[int]
    OUTSIDE_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    SENSOR_BLINDNESS_FIELD_NUMBER: _ClassVar[int]
    SENSITIVITY_FIELD_NUMBER: _ClassVar[int]
    SENSOR_FAULTED_FIELD_NUMBER: _ClassVar[int]
    FAILURE_STATUS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    number_sensors: int
    sending_pattern: int
    operating_mode: int
    outside_temperature: float
    sensor_blindness: int
    sensitivity: int
    sensor_faulted: int
    failure_status: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., number_sensors: _Optional[int] = ..., sending_pattern: _Optional[int] = ..., operating_mode: _Optional[int] = ..., outside_temperature: _Optional[float] = ..., sensor_blindness: _Optional[int] = ..., sensitivity: _Optional[int] = ..., sensor_faulted: _Optional[int] = ..., failure_status: bool = ...) -> None: ...
