from make87_messages_ros2.rolling.geometry_msgs.msg import pose_pb2 as _pose_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Node(_message.Message):
    __slots__ = ["id", "valid", "pose", "flags"]
    ID_FIELD_NUMBER: _ClassVar[int]
    VALID_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    id: int
    valid: bool
    pose: _pose_pb2.Pose
    flags: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, id: _Optional[int] = ..., valid: bool = ..., pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., flags: _Optional[_Iterable[int]] = ...) -> None: ...
