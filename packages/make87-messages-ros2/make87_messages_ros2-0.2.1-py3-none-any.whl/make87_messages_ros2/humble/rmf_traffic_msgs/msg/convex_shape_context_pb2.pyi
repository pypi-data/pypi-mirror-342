from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rmf_traffic_msgs.msg import circle_pb2 as _circle_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ConvexShapeContext(_message.Message):
    __slots__ = ["header", "circles"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CIRCLES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    circles: _containers.RepeatedCompositeFieldContainer[_circle_pb2.Circle]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., circles: _Optional[_Iterable[_Union[_circle_pb2.Circle, _Mapping]]] = ...) -> None: ...
