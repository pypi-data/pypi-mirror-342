from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import duration_pb2 as _duration_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AudioNote(_message.Message):
    __slots__ = ["header", "frequency", "max_runtime"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FREQUENCY_FIELD_NUMBER: _ClassVar[int]
    MAX_RUNTIME_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    frequency: int
    max_runtime: _duration_pb2.Duration
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., frequency: _Optional[int] = ..., max_runtime: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...) -> None: ...
