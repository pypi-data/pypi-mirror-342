from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import point_pb2 as _point_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import quaternion_pb2 as _quaternion_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Pose(_message.Message):
    __slots__ = ["header", "position", "orientation"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    position: _point_pb2.Point
    orientation: _quaternion_pb2.Quaternion
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., position: _Optional[_Union[_point_pb2.Point, _Mapping]] = ..., orientation: _Optional[_Union[_quaternion_pb2.Quaternion, _Mapping]] = ...) -> None: ...
