from make87_messages_ros2.jazzy.geometry_msgs.msg import point_pb2 as _point_pb2
from make87_messages_ros2.jazzy.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PositionTarget(_message.Message):
    __slots__ = ["header", "coordinate_frame", "type_mask", "position", "velocity", "acceleration_or_force", "yaw", "yaw_rate"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    COORDINATE_FRAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_MASK_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_FIELD_NUMBER: _ClassVar[int]
    ACCELERATION_OR_FORCE_FIELD_NUMBER: _ClassVar[int]
    YAW_FIELD_NUMBER: _ClassVar[int]
    YAW_RATE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    coordinate_frame: int
    type_mask: int
    position: _point_pb2.Point
    velocity: _vector3_pb2.Vector3
    acceleration_or_force: _vector3_pb2.Vector3
    yaw: float
    yaw_rate: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., coordinate_frame: _Optional[int] = ..., type_mask: _Optional[int] = ..., position: _Optional[_Union[_point_pb2.Point, _Mapping]] = ..., velocity: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., acceleration_or_force: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., yaw: _Optional[float] = ..., yaw_rate: _Optional[float] = ...) -> None: ...
