from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TeleopState(_message.Message):
    __slots__ = ["header", "teleop_signals"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TELEOP_SIGNALS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    teleop_signals: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., teleop_signals: _Optional[_Iterable[int]] = ...) -> None: ...
