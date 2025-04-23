from make87_messages_ros2.rolling.nav_msgs.msg import occupancy_grid_pb2 as _occupancy_grid_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetGridmapLayerRequest(_message.Message):
    __slots__ = ["layer_name"]
    LAYER_NAME_FIELD_NUMBER: _ClassVar[int]
    layer_name: str
    def __init__(self, layer_name: _Optional[str] = ...) -> None: ...

class GetGridmapLayerResponse(_message.Message):
    __slots__ = ["valid", "grid"]
    VALID_FIELD_NUMBER: _ClassVar[int]
    GRID_FIELD_NUMBER: _ClassVar[int]
    valid: bool
    grid: _occupancy_grid_pb2.OccupancyGrid
    def __init__(self, valid: bool = ..., grid: _Optional[_Union[_occupancy_grid_pb2.OccupancyGrid, _Mapping]] = ...) -> None: ...
