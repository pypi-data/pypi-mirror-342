from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PrimaryFeedback(_message.Message):
    __slots__ = ["header", "present", "robotic_mode", "steering_command", "steering_measure", "throttle_command", "throttle_measure", "brake_command", "brake_measure", "estop_command", "estop_measure", "error_steering", "error_throttle", "error_brake", "error_other"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PRESENT_FIELD_NUMBER: _ClassVar[int]
    ROBOTIC_MODE_FIELD_NUMBER: _ClassVar[int]
    STEERING_COMMAND_FIELD_NUMBER: _ClassVar[int]
    STEERING_MEASURE_FIELD_NUMBER: _ClassVar[int]
    THROTTLE_COMMAND_FIELD_NUMBER: _ClassVar[int]
    THROTTLE_MEASURE_FIELD_NUMBER: _ClassVar[int]
    BRAKE_COMMAND_FIELD_NUMBER: _ClassVar[int]
    BRAKE_MEASURE_FIELD_NUMBER: _ClassVar[int]
    ESTOP_COMMAND_FIELD_NUMBER: _ClassVar[int]
    ESTOP_MEASURE_FIELD_NUMBER: _ClassVar[int]
    ERROR_STEERING_FIELD_NUMBER: _ClassVar[int]
    ERROR_THROTTLE_FIELD_NUMBER: _ClassVar[int]
    ERROR_BRAKE_FIELD_NUMBER: _ClassVar[int]
    ERROR_OTHER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    present: bool
    robotic_mode: bool
    steering_command: float
    steering_measure: float
    throttle_command: float
    throttle_measure: float
    brake_command: float
    brake_measure: float
    estop_command: bool
    estop_measure: bool
    error_steering: bool
    error_throttle: bool
    error_brake: bool
    error_other: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., present: bool = ..., robotic_mode: bool = ..., steering_command: _Optional[float] = ..., steering_measure: _Optional[float] = ..., throttle_command: _Optional[float] = ..., throttle_measure: _Optional[float] = ..., brake_command: _Optional[float] = ..., brake_measure: _Optional[float] = ..., estop_command: bool = ..., estop_measure: bool = ..., error_steering: bool = ..., error_throttle: bool = ..., error_brake: bool = ..., error_other: bool = ...) -> None: ...
