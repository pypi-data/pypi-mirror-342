from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_pb2 as _pose_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RouteSegment(_message.Message):
    __slots__ = ["header", "id", "type", "orientation", "motion_type", "start", "end", "center", "level"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    MOTION_TYPE_FIELD_NUMBER: _ClassVar[int]
    START_FIELD_NUMBER: _ClassVar[int]
    END_FIELD_NUMBER: _ClassVar[int]
    CENTER_FIELD_NUMBER: _ClassVar[int]
    LEVEL_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    id: int
    type: int
    orientation: int
    motion_type: int
    start: _pose_pb2.Pose
    end: _pose_pb2.Pose
    center: _pose_pb2.Pose
    level: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., id: _Optional[int] = ..., type: _Optional[int] = ..., orientation: _Optional[int] = ..., motion_type: _Optional[int] = ..., start: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., end: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., center: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., level: _Optional[int] = ...) -> None: ...
