from make87_messages_ros2.rolling.sensor_msgs.msg import point_cloud2_pb2 as _point_cloud2_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetPointMapROIRequest(_message.Message):
    __slots__ = ["x", "y", "z", "r", "l_x", "l_y", "l_z"]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    R_FIELD_NUMBER: _ClassVar[int]
    L_X_FIELD_NUMBER: _ClassVar[int]
    L_Y_FIELD_NUMBER: _ClassVar[int]
    L_Z_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    z: float
    r: float
    l_x: float
    l_y: float
    l_z: float
    def __init__(self, x: _Optional[float] = ..., y: _Optional[float] = ..., z: _Optional[float] = ..., r: _Optional[float] = ..., l_x: _Optional[float] = ..., l_y: _Optional[float] = ..., l_z: _Optional[float] = ...) -> None: ...

class GetPointMapROIResponse(_message.Message):
    __slots__ = ["sub_map"]
    SUB_MAP_FIELD_NUMBER: _ClassVar[int]
    sub_map: _point_cloud2_pb2.PointCloud2
    def __init__(self, sub_map: _Optional[_Union[_point_cloud2_pb2.PointCloud2, _Mapping]] = ...) -> None: ...
