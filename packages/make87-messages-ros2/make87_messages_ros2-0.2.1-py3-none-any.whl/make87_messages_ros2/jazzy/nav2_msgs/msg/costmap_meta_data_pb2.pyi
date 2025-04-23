from make87_messages_ros2.jazzy.builtin_interfaces.msg import time_pb2 as _time_pb2
from make87_messages_ros2.jazzy.geometry_msgs.msg import pose_pb2 as _pose_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CostmapMetaData(_message.Message):
    __slots__ = ["map_load_time", "update_time", "layer", "resolution", "size_x", "size_y", "origin"]
    MAP_LOAD_TIME_FIELD_NUMBER: _ClassVar[int]
    UPDATE_TIME_FIELD_NUMBER: _ClassVar[int]
    LAYER_FIELD_NUMBER: _ClassVar[int]
    RESOLUTION_FIELD_NUMBER: _ClassVar[int]
    SIZE_X_FIELD_NUMBER: _ClassVar[int]
    SIZE_Y_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    map_load_time: _time_pb2.Time
    update_time: _time_pb2.Time
    layer: str
    resolution: float
    size_x: int
    size_y: int
    origin: _pose_pb2.Pose
    def __init__(self, map_load_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., update_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., layer: _Optional[str] = ..., resolution: _Optional[float] = ..., size_x: _Optional[int] = ..., size_y: _Optional[int] = ..., origin: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ...) -> None: ...
