from make87_messages_ros2.rolling.rmf_traffic_msgs.msg import trajectory_waypoint_pb2 as _trajectory_waypoint_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Trajectory(_message.Message):
    __slots__ = ["waypoints"]
    WAYPOINTS_FIELD_NUMBER: _ClassVar[int]
    waypoints: _containers.RepeatedCompositeFieldContainer[_trajectory_waypoint_pb2.TrajectoryWaypoint]
    def __init__(self, waypoints: _Optional[_Iterable[_Union[_trajectory_waypoint_pb2.TrajectoryWaypoint, _Mapping]]] = ...) -> None: ...
