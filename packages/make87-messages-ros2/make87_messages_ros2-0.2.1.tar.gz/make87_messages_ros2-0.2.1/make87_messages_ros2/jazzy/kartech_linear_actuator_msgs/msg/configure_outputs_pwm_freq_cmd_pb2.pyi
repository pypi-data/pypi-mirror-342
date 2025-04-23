from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ConfigureOutputsPwmFreqCmd(_message.Message):
    __slots__ = ["header", "confirm", "min_pwm_pct", "max_pwm_pct", "pwm_freq"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CONFIRM_FIELD_NUMBER: _ClassVar[int]
    MIN_PWM_PCT_FIELD_NUMBER: _ClassVar[int]
    MAX_PWM_PCT_FIELD_NUMBER: _ClassVar[int]
    PWM_FREQ_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    confirm: bool
    min_pwm_pct: int
    max_pwm_pct: int
    pwm_freq: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., confirm: bool = ..., min_pwm_pct: _Optional[int] = ..., max_pwm_pct: _Optional[int] = ..., pwm_freq: _Optional[int] = ...) -> None: ...
