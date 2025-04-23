from make87_messages_ros2.jazzy.mavros_msgs.msg import position_target_pb2 as _position_target_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Trajectory(_message.Message):
    __slots__ = ["header", "type", "point_1", "point_2", "point_3", "point_4", "point_5", "point_valid", "command", "time_horizon"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    POINT_1_FIELD_NUMBER: _ClassVar[int]
    POINT_2_FIELD_NUMBER: _ClassVar[int]
    POINT_3_FIELD_NUMBER: _ClassVar[int]
    POINT_4_FIELD_NUMBER: _ClassVar[int]
    POINT_5_FIELD_NUMBER: _ClassVar[int]
    POINT_VALID_FIELD_NUMBER: _ClassVar[int]
    COMMAND_FIELD_NUMBER: _ClassVar[int]
    TIME_HORIZON_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    type: int
    point_1: _position_target_pb2.PositionTarget
    point_2: _position_target_pb2.PositionTarget
    point_3: _position_target_pb2.PositionTarget
    point_4: _position_target_pb2.PositionTarget
    point_5: _position_target_pb2.PositionTarget
    point_valid: _containers.RepeatedScalarFieldContainer[int]
    command: _containers.RepeatedScalarFieldContainer[int]
    time_horizon: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., type: _Optional[int] = ..., point_1: _Optional[_Union[_position_target_pb2.PositionTarget, _Mapping]] = ..., point_2: _Optional[_Union[_position_target_pb2.PositionTarget, _Mapping]] = ..., point_3: _Optional[_Union[_position_target_pb2.PositionTarget, _Mapping]] = ..., point_4: _Optional[_Union[_position_target_pb2.PositionTarget, _Mapping]] = ..., point_5: _Optional[_Union[_position_target_pb2.PositionTarget, _Mapping]] = ..., point_valid: _Optional[_Iterable[int]] = ..., command: _Optional[_Iterable[int]] = ..., time_horizon: _Optional[_Iterable[float]] = ...) -> None: ...
