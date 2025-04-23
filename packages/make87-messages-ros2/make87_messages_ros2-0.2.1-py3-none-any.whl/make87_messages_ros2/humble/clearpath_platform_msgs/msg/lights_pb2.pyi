from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.clearpath_platform_msgs.msg import rgb_pb2 as _rgb_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Lights(_message.Message):
    __slots__ = ["header", "lights"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    LIGHTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    lights: _containers.RepeatedCompositeFieldContainer[_rgb_pb2.RGB]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., lights: _Optional[_Iterable[_Union[_rgb_pb2.RGB, _Mapping]]] = ...) -> None: ...
