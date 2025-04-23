from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class TrajectoryPoint(_message.Message):
    __slots__ = ["header", "position", "twist", "acceleration", "yaw_angle"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    POSITION_FIELD_NUMBER: _ClassVar[int]
    TWIST_FIELD_NUMBER: _ClassVar[int]
    ACCELERATION_FIELD_NUMBER: _ClassVar[int]
    YAW_ANGLE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    position: _vector3_pb2.Vector3
    twist: _vector3_pb2.Vector3
    acceleration: _vector3_pb2.Vector3
    yaw_angle: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., position: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., twist: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., acceleration: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ..., yaw_angle: _Optional[float] = ...) -> None: ...
