from make87_messages_ros2.rolling.geometry_msgs.msg import pose_pb2 as _pose_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LandmarkEntry(_message.Message):
    __slots__ = ["id", "tracking_from_landmark_transform", "translation_weight", "rotation_weight"]
    ID_FIELD_NUMBER: _ClassVar[int]
    TRACKING_FROM_LANDMARK_TRANSFORM_FIELD_NUMBER: _ClassVar[int]
    TRANSLATION_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    ROTATION_WEIGHT_FIELD_NUMBER: _ClassVar[int]
    id: str
    tracking_from_landmark_transform: _pose_pb2.Pose
    translation_weight: float
    rotation_weight: float
    def __init__(self, id: _Optional[str] = ..., tracking_from_landmark_transform: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., translation_weight: _Optional[float] = ..., rotation_weight: _Optional[float] = ...) -> None: ...
