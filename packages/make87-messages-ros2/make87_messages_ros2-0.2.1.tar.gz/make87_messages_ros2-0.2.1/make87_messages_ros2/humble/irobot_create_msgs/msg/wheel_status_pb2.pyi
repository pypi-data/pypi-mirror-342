from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class WheelStatus(_message.Message):
    __slots__ = ["header", "ros2_header", "current_ma_left", "current_ma_right", "pwm_left", "pwm_right", "wheels_enabled"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    CURRENT_MA_LEFT_FIELD_NUMBER: _ClassVar[int]
    CURRENT_MA_RIGHT_FIELD_NUMBER: _ClassVar[int]
    PWM_LEFT_FIELD_NUMBER: _ClassVar[int]
    PWM_RIGHT_FIELD_NUMBER: _ClassVar[int]
    WHEELS_ENABLED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    current_ma_left: int
    current_ma_right: int
    pwm_left: int
    pwm_right: int
    wheels_enabled: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., current_ma_left: _Optional[int] = ..., current_ma_right: _Optional[int] = ..., pwm_left: _Optional[int] = ..., pwm_right: _Optional[int] = ..., wheels_enabled: bool = ...) -> None: ...
