from make87_messages_ros2.rolling.autoware_planning_msgs.msg import path_point_pb2 as _path_point_pb2
from make87_messages_ros2.rolling.geometry_msgs.msg import point_pb2 as _point_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Path(_message.Message):
    __slots__ = ["header", "points", "left_bound", "right_bound"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    POINTS_FIELD_NUMBER: _ClassVar[int]
    LEFT_BOUND_FIELD_NUMBER: _ClassVar[int]
    RIGHT_BOUND_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    points: _containers.RepeatedCompositeFieldContainer[_path_point_pb2.PathPoint]
    left_bound: _containers.RepeatedCompositeFieldContainer[_point_pb2.Point]
    right_bound: _containers.RepeatedCompositeFieldContainer[_point_pb2.Point]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., points: _Optional[_Iterable[_Union[_path_point_pb2.PathPoint, _Mapping]]] = ..., left_bound: _Optional[_Iterable[_Union[_point_pb2.Point, _Mapping]]] = ..., right_bound: _Optional[_Iterable[_Union[_point_pb2.Point, _Mapping]]] = ...) -> None: ...
