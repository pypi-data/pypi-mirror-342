from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import point_stamped_pb2 as _point_stamped_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LookAtWithStyle(_message.Message):
    __slots__ = ["header", "style", "target"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    STYLE_FIELD_NUMBER: _ClassVar[int]
    TARGET_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    style: int
    target: _point_stamped_pb2.PointStamped
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., style: _Optional[int] = ..., target: _Optional[_Union[_point_stamped_pb2.PointStamped, _Mapping]] = ...) -> None: ...
