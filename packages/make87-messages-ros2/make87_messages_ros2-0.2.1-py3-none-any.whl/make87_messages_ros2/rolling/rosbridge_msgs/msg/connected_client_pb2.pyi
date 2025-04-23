from make87_messages_ros2.rolling.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ConnectedClient(_message.Message):
    __slots__ = ["ip_address", "connection_time"]
    IP_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_TIME_FIELD_NUMBER: _ClassVar[int]
    ip_address: str
    connection_time: _time_pb2.Time
    def __init__(self, ip_address: _Optional[str] = ..., connection_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ...) -> None: ...
