from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SteeringCmd(_message.Message):
    __slots__ = ["header", "ros2_header", "cmd", "cmd_rate", "cmd_accel", "cmd_type", "enable", "clear", "ignore"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    CMD_FIELD_NUMBER: _ClassVar[int]
    CMD_RATE_FIELD_NUMBER: _ClassVar[int]
    CMD_ACCEL_FIELD_NUMBER: _ClassVar[int]
    CMD_TYPE_FIELD_NUMBER: _ClassVar[int]
    ENABLE_FIELD_NUMBER: _ClassVar[int]
    CLEAR_FIELD_NUMBER: _ClassVar[int]
    IGNORE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    cmd: float
    cmd_rate: float
    cmd_accel: float
    cmd_type: int
    enable: bool
    clear: bool
    ignore: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., cmd: _Optional[float] = ..., cmd_rate: _Optional[float] = ..., cmd_accel: _Optional[float] = ..., cmd_type: _Optional[int] = ..., enable: bool = ..., clear: bool = ..., ignore: bool = ...) -> None: ...
