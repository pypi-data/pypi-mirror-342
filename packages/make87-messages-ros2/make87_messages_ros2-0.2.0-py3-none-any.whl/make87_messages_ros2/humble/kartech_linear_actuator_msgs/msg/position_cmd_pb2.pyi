from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PositionCmd(_message.Message):
    __slots__ = ["header", "ros2_header", "confirm", "auto_reply", "position", "clutch_enable", "motor_enable"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    CONFIRM_FIELD_NUMBER: _ClassVar[int]
    AUTO_REPLY_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    CLUTCH_ENABLE_FIELD_NUMBER: _ClassVar[int]
    MOTOR_ENABLE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    confirm: bool
    auto_reply: bool
    position: float
    clutch_enable: bool
    motor_enable: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., confirm: bool = ..., auto_reply: bool = ..., position: _Optional[float] = ..., clutch_enable: bool = ..., motor_enable: bool = ...) -> None: ...
