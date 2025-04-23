from make87_messages_ros2.rolling.geometry_msgs.msg import pose_with_covariance_stamped_pb2 as _pose_with_covariance_stamped_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetPoseRequest(_message.Message):
    __slots__ = ["pose"]
    POSE_FIELD_NUMBER: _ClassVar[int]
    pose: _pose_with_covariance_stamped_pb2.PoseWithCovarianceStamped
    def __init__(self, pose: _Optional[_Union[_pose_with_covariance_stamped_pb2.PoseWithCovarianceStamped, _Mapping]] = ...) -> None: ...

class SetPoseResponse(_message.Message):
    __slots__ = ["success", "message"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...
