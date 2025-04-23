from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rcss3d_agent_msgs.msg import spherical_pb2 as _spherical_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Goalpost(_message.Message):
    __slots__ = ["header", "name", "top"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TOP_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    name: str
    top: _spherical_pb2.Spherical
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., name: _Optional[str] = ..., top: _Optional[_Union[_spherical_pb2.Spherical, _Mapping]] = ...) -> None: ...
