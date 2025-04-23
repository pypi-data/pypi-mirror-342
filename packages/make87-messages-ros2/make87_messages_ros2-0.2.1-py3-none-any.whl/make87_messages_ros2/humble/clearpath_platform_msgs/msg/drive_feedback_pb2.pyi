from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DriveFeedback(_message.Message):
    __slots__ = ["header", "current", "duty_cycle", "bridge_temperature", "motor_temperature", "measured_velocity", "measured_travel", "driver_fault"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CURRENT_FIELD_NUMBER: _ClassVar[int]
    DUTY_CYCLE_FIELD_NUMBER: _ClassVar[int]
    BRIDGE_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    MOTOR_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    MEASURED_VELOCITY_FIELD_NUMBER: _ClassVar[int]
    MEASURED_TRAVEL_FIELD_NUMBER: _ClassVar[int]
    DRIVER_FAULT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    current: float
    duty_cycle: float
    bridge_temperature: float
    motor_temperature: float
    measured_velocity: float
    measured_travel: float
    driver_fault: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., current: _Optional[float] = ..., duty_cycle: _Optional[float] = ..., bridge_temperature: _Optional[float] = ..., motor_temperature: _Optional[float] = ..., measured_velocity: _Optional[float] = ..., measured_travel: _Optional[float] = ..., driver_fault: bool = ...) -> None: ...
