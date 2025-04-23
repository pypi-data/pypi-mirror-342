from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EmergencyStopState(_message.Message):
    __slots__ = ["header", "emergency_button_stop", "scanner_stop", "monitoring_stop", "user_interaction_stop", "hardware_stop", "bumper_stop", "fall_stop", "charge_stop", "emergency_state"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    EMERGENCY_BUTTON_STOP_FIELD_NUMBER: _ClassVar[int]
    SCANNER_STOP_FIELD_NUMBER: _ClassVar[int]
    MONITORING_STOP_FIELD_NUMBER: _ClassVar[int]
    USER_INTERACTION_STOP_FIELD_NUMBER: _ClassVar[int]
    HARDWARE_STOP_FIELD_NUMBER: _ClassVar[int]
    BUMPER_STOP_FIELD_NUMBER: _ClassVar[int]
    FALL_STOP_FIELD_NUMBER: _ClassVar[int]
    CHARGE_STOP_FIELD_NUMBER: _ClassVar[int]
    EMERGENCY_STATE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    emergency_button_stop: bool
    scanner_stop: bool
    monitoring_stop: bool
    user_interaction_stop: bool
    hardware_stop: bool
    bumper_stop: bool
    fall_stop: bool
    charge_stop: bool
    emergency_state: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., emergency_button_stop: bool = ..., scanner_stop: bool = ..., monitoring_stop: bool = ..., user_interaction_stop: bool = ..., hardware_stop: bool = ..., bumper_stop: bool = ..., fall_stop: bool = ..., charge_stop: bool = ..., emergency_state: _Optional[int] = ...) -> None: ...
