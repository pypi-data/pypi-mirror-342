from make87_messages_ros2.rolling.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LandingTarget(_message.Message):
    __slots__ = ["header", "target_num", "frame", "angle", "distance", "size", "pose", "type"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TARGET_NUM_FIELD_NUMBER: _ClassVar[int]
    FRAME_FIELD_NUMBER: _ClassVar[int]
    ANGLE_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    target_num: int
    frame: int
    angle: _containers.RepeatedScalarFieldContainer[float]
    distance: float
    size: _containers.RepeatedScalarFieldContainer[float]
    pose: _pose_pb2.Pose
    type: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., target_num: _Optional[int] = ..., frame: _Optional[int] = ..., angle: _Optional[_Iterable[float]] = ..., distance: _Optional[float] = ..., size: _Optional[_Iterable[float]] = ..., pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., type: _Optional[int] = ...) -> None: ...
