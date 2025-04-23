from make87_messages_ros2.rolling.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.rolling.marti_nav_msgs.msg import route_position_pb2 as _route_position_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RouteOffset(_message.Message):
    __slots__ = ["header", "relative_pose", "route_position"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    RELATIVE_POSE_FIELD_NUMBER: _ClassVar[int]
    ROUTE_POSITION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    relative_pose: _pose_pb2.Pose
    route_position: _route_position_pb2.RoutePosition
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., relative_pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., route_position: _Optional[_Union[_route_position_pb2.RoutePosition, _Mapping]] = ...) -> None: ...
