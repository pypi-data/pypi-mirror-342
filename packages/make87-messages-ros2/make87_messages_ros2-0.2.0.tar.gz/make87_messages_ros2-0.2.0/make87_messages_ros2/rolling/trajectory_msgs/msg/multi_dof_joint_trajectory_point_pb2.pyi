from make87_messages_ros2.rolling.builtin_interfaces.msg import duration_pb2 as _duration_pb2
from make87_messages_ros2.rolling.geometry_msgs.msg import transform_pb2 as _transform_pb2
from make87_messages_ros2.rolling.geometry_msgs.msg import twist_pb2 as _twist_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MultiDOFJointTrajectoryPoint(_message.Message):
    __slots__ = ["transforms", "velocities", "accelerations", "time_from_start"]
    TRANSFORMS_FIELD_NUMBER: _ClassVar[int]
    VELOCITIES_FIELD_NUMBER: _ClassVar[int]
    ACCELERATIONS_FIELD_NUMBER: _ClassVar[int]
    TIME_FROM_START_FIELD_NUMBER: _ClassVar[int]
    transforms: _containers.RepeatedCompositeFieldContainer[_transform_pb2.Transform]
    velocities: _containers.RepeatedCompositeFieldContainer[_twist_pb2.Twist]
    accelerations: _containers.RepeatedCompositeFieldContainer[_twist_pb2.Twist]
    time_from_start: _duration_pb2.Duration
    def __init__(self, transforms: _Optional[_Iterable[_Union[_transform_pb2.Transform, _Mapping]]] = ..., velocities: _Optional[_Iterable[_Union[_twist_pb2.Twist, _Mapping]]] = ..., accelerations: _Optional[_Iterable[_Union[_twist_pb2.Twist, _Mapping]]] = ..., time_from_start: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...) -> None: ...
