from make87_messages_ros2.jazzy.geometry_msgs.msg import pose_stamped_pb2 as _pose_stamped_pb2
from make87_messages_ros2.jazzy.rtabmap_msgs.msg import path_pb2 as _path_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetPlanRequest(_message.Message):
    __slots__ = ["goal_node", "goal", "tolerance"]
    GOAL_NODE_FIELD_NUMBER: _ClassVar[int]
    GOAL_FIELD_NUMBER: _ClassVar[int]
    TOLERANCE_FIELD_NUMBER: _ClassVar[int]
    goal_node: int
    goal: _pose_stamped_pb2.PoseStamped
    tolerance: float
    def __init__(self, goal_node: _Optional[int] = ..., goal: _Optional[_Union[_pose_stamped_pb2.PoseStamped, _Mapping]] = ..., tolerance: _Optional[float] = ...) -> None: ...

class GetPlanResponse(_message.Message):
    __slots__ = ["plan"]
    PLAN_FIELD_NUMBER: _ClassVar[int]
    plan: _path_pb2.Path
    def __init__(self, plan: _Optional[_Union[_path_pb2.Path, _Mapping]] = ...) -> None: ...
