from make87_messages_ros2.rolling.geometry_msgs.msg import pose_pb2 as _pose_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Marker(_message.Message):
    __slots__ = ["ids", "ids_confidence", "pose"]
    IDS_FIELD_NUMBER: _ClassVar[int]
    IDS_CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    ids: _containers.RepeatedScalarFieldContainer[int]
    ids_confidence: _containers.RepeatedScalarFieldContainer[float]
    pose: _pose_pb2.Pose
    def __init__(self, ids: _Optional[_Iterable[int]] = ..., ids_confidence: _Optional[_Iterable[float]] = ..., pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ...) -> None: ...
