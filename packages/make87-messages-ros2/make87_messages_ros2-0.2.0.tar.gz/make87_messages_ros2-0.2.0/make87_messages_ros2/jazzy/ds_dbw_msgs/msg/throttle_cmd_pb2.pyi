from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ThrottleCmd(_message.Message):
    __slots__ = ["header", "cmd", "rate_inc", "rate_dec", "cmd_type", "enable", "clear", "ignore"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CMD_FIELD_NUMBER: _ClassVar[int]
    RATE_INC_FIELD_NUMBER: _ClassVar[int]
    RATE_DEC_FIELD_NUMBER: _ClassVar[int]
    CMD_TYPE_FIELD_NUMBER: _ClassVar[int]
    ENABLE_FIELD_NUMBER: _ClassVar[int]
    CLEAR_FIELD_NUMBER: _ClassVar[int]
    IGNORE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    cmd: float
    rate_inc: float
    rate_dec: float
    cmd_type: int
    enable: bool
    clear: bool
    ignore: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., cmd: _Optional[float] = ..., rate_inc: _Optional[float] = ..., rate_dec: _Optional[float] = ..., cmd_type: _Optional[int] = ..., enable: bool = ..., clear: bool = ..., ignore: bool = ...) -> None: ...
