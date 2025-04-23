from make87_messages_ros2.rolling.nav_msgs.msg import occupancy_grid_pb2 as _occupancy_grid_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ProjectedMap(_message.Message):
    __slots__ = ["map", "min_z", "max_z"]
    MAP_FIELD_NUMBER: _ClassVar[int]
    MIN_Z_FIELD_NUMBER: _ClassVar[int]
    MAX_Z_FIELD_NUMBER: _ClassVar[int]
    map: _occupancy_grid_pb2.OccupancyGrid
    min_z: float
    max_z: float
    def __init__(self, map: _Optional[_Union[_occupancy_grid_pb2.OccupancyGrid, _Mapping]] = ..., min_z: _Optional[float] = ..., max_z: _Optional[float] = ...) -> None: ...
