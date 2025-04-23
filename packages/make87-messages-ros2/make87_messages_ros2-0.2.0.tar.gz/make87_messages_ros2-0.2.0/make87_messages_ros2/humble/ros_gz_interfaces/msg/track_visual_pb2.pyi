from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TrackVisual(_message.Message):
    __slots__ = ["header", "ros2_header", "name", "id", "inherit_orientation", "min_dist", "max_dist", "is_static", "use_model_frame", "xyz", "inherit_yaw"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    INHERIT_ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    MIN_DIST_FIELD_NUMBER: _ClassVar[int]
    MAX_DIST_FIELD_NUMBER: _ClassVar[int]
    IS_STATIC_FIELD_NUMBER: _ClassVar[int]
    USE_MODEL_FRAME_FIELD_NUMBER: _ClassVar[int]
    XYZ_FIELD_NUMBER: _ClassVar[int]
    INHERIT_YAW_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    name: str
    id: int
    inherit_orientation: bool
    min_dist: float
    max_dist: float
    is_static: bool
    use_model_frame: bool
    xyz: _vector3_pb2.Vector3
    inherit_yaw: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., name: _Optional[str] = ..., id: _Optional[int] = ..., inherit_orientation: bool = ..., min_dist: _Optional[float] = ..., max_dist: _Optional[float] = ..., is_static: bool = ..., use_model_frame: bool = ..., xyz: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., inherit_yaw: bool = ...) -> None: ...
