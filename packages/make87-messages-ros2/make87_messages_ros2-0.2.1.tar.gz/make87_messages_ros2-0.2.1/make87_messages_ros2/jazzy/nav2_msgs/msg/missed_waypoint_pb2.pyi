from make87_messages_ros2.jazzy.geometry_msgs.msg import pose_stamped_pb2 as _pose_stamped_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MissedWaypoint(_message.Message):
    __slots__ = ["index", "goal", "error_code"]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    GOAL_FIELD_NUMBER: _ClassVar[int]
    ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    index: int
    goal: _pose_stamped_pb2.PoseStamped
    error_code: int
    def __init__(self, index: _Optional[int] = ..., goal: _Optional[_Union[_pose_stamped_pb2.PoseStamped, _Mapping]] = ..., error_code: _Optional[int] = ...) -> None: ...
