from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TestSubArray(_message.Message):
    __slots__ = ["header", "ints", "strings", "times"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    INTS_FIELD_NUMBER: _ClassVar[int]
    STRINGS_FIELD_NUMBER: _ClassVar[int]
    TIMES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ints: _containers.RepeatedScalarFieldContainer[int]
    strings: _containers.RepeatedScalarFieldContainer[str]
    times: _containers.RepeatedCompositeFieldContainer[_time_pb2.Time]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ints: _Optional[_Iterable[int]] = ..., strings: _Optional[_Iterable[str]] = ..., times: _Optional[_Iterable[_Union[_time_pb2.Time, _Mapping]]] = ...) -> None: ...
