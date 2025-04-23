from make87_messages_ros2.rolling.geometry_msgs.msg import inertia_pb2 as _inertia_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class InertiaStamped(_message.Message):
    __slots__ = ["header", "inertia"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    INERTIA_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    inertia: _inertia_pb2.Inertia
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., inertia: _Optional[_Union[_inertia_pb2.Inertia, _Mapping]] = ...) -> None: ...
