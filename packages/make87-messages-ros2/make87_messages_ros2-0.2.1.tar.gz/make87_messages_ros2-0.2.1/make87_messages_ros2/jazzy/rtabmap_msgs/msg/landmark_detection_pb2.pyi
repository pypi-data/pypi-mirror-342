from make87_messages_ros2.jazzy.geometry_msgs.msg import pose_with_covariance_pb2 as _pose_with_covariance_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LandmarkDetection(_message.Message):
    __slots__ = ["header", "landmark_frame_id", "id", "size", "pose"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    LANDMARK_FRAME_ID_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    SIZE_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    landmark_frame_id: str
    id: int
    size: float
    pose: _pose_with_covariance_pb2.PoseWithCovariance
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., landmark_frame_id: _Optional[str] = ..., id: _Optional[int] = ..., size: _Optional[float] = ..., pose: _Optional[_Union[_pose_with_covariance_pb2.PoseWithCovariance, _Mapping]] = ...) -> None: ...
