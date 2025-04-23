from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class WheelOdom(_message.Message):
    __slots__ = ["header", "stamp", "velocity_lin", "velocity_ang", "pose_x", "pose_y", "pose_yaw"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    STAMP_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_LIN_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_ANG_FIELD_NUMBER: _ClassVar[int]
    POSE_X_FIELD_NUMBER: _ClassVar[int]
    POSE_Y_FIELD_NUMBER: _ClassVar[int]
    POSE_YAW_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    stamp: _time_pb2.Time
    velocity_lin: float
    velocity_ang: float
    pose_x: float
    pose_y: float
    pose_yaw: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., stamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., velocity_lin: _Optional[float] = ..., velocity_ang: _Optional[float] = ..., pose_x: _Optional[float] = ..., pose_y: _Optional[float] = ..., pose_yaw: _Optional[float] = ...) -> None: ...
