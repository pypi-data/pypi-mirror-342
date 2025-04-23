from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ConnectedClient(_message.Message):
    __slots__ = ["header", "ip_address", "connection_time"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_TIME_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ip_address: str
    connection_time: _time_pb2.Time
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ip_address: _Optional[str] = ..., connection_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ...) -> None: ...
