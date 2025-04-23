from make87_messages_ros2.jazzy.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.jazzy.moveit_msgs.msg import constraints_pb2 as _constraints_pb2
from make87_messages_ros2.jazzy.moveit_msgs.msg import move_it_error_codes_pb2 as _move_it_error_codes_pb2
from make87_messages_ros2.jazzy.moveit_msgs.msg import robot_state_pb2 as _robot_state_pb2
from make87_messages_ros2.jazzy.moveit_msgs.msg import robot_trajectory_pb2 as _robot_trajectory_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetCartesianPathRequest(_message.Message):
    __slots__ = ["header", "start_state", "group_name", "link_name", "waypoints", "max_step", "jump_threshold", "prismatic_jump_threshold", "revolute_jump_threshold", "avoid_collisions", "path_constraints", "max_velocity_scaling_factor", "max_acceleration_scaling_factor", "cartesian_speed_limited_link", "max_cartesian_speed"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    START_STATE_FIELD_NUMBER: _ClassVar[int]
    GROUP_NAME_FIELD_NUMBER: _ClassVar[int]
    LINK_NAME_FIELD_NUMBER: _ClassVar[int]
    WAYPOINTS_FIELD_NUMBER: _ClassVar[int]
    MAX_STEP_FIELD_NUMBER: _ClassVar[int]
    JUMP_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    PRISMATIC_JUMP_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    REVOLUTE_JUMP_THRESHOLD_FIELD_NUMBER: _ClassVar[int]
    AVOID_COLLISIONS_FIELD_NUMBER: _ClassVar[int]
    PATH_CONSTRAINTS_FIELD_NUMBER: _ClassVar[int]
    MAX_VELOCITY_SCALING_FACTOR_FIELD_NUMBER: _ClassVar[int]
    MAX_ACCELERATION_SCALING_FACTOR_FIELD_NUMBER: _ClassVar[int]
    CARTESIAN_SPEED_LIMITED_LINK_FIELD_NUMBER: _ClassVar[int]
    MAX_CARTESIAN_SPEED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    start_state: _robot_state_pb2.RobotState
    group_name: str
    link_name: str
    waypoints: _containers.RepeatedCompositeFieldContainer[_pose_pb2.Pose]
    max_step: float
    jump_threshold: float
    prismatic_jump_threshold: float
    revolute_jump_threshold: float
    avoid_collisions: bool
    path_constraints: _constraints_pb2.Constraints
    max_velocity_scaling_factor: float
    max_acceleration_scaling_factor: float
    cartesian_speed_limited_link: str
    max_cartesian_speed: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., start_state: _Optional[_Union[_robot_state_pb2.RobotState, _Mapping]] = ..., group_name: _Optional[str] = ..., link_name: _Optional[str] = ..., waypoints: _Optional[_Iterable[_Union[_pose_pb2.Pose, _Mapping]]] = ..., max_step: _Optional[float] = ..., jump_threshold: _Optional[float] = ..., prismatic_jump_threshold: _Optional[float] = ..., revolute_jump_threshold: _Optional[float] = ..., avoid_collisions: bool = ..., path_constraints: _Optional[_Union[_constraints_pb2.Constraints, _Mapping]] = ..., max_velocity_scaling_factor: _Optional[float] = ..., max_acceleration_scaling_factor: _Optional[float] = ..., cartesian_speed_limited_link: _Optional[str] = ..., max_cartesian_speed: _Optional[float] = ...) -> None: ...

class GetCartesianPathResponse(_message.Message):
    __slots__ = ["start_state", "solution", "fraction", "error_code"]
    START_STATE_FIELD_NUMBER: _ClassVar[int]
    SOLUTION_FIELD_NUMBER: _ClassVar[int]
    FRACTION_FIELD_NUMBER: _ClassVar[int]
    ERROR_CODE_FIELD_NUMBER: _ClassVar[int]
    start_state: _robot_state_pb2.RobotState
    solution: _robot_trajectory_pb2.RobotTrajectory
    fraction: float
    error_code: _move_it_error_codes_pb2.MoveItErrorCodes
    def __init__(self, start_state: _Optional[_Union[_robot_state_pb2.RobotState, _Mapping]] = ..., solution: _Optional[_Union[_robot_trajectory_pb2.RobotTrajectory, _Mapping]] = ..., fraction: _Optional[float] = ..., error_code: _Optional[_Union[_move_it_error_codes_pb2.MoveItErrorCodes, _Mapping]] = ...) -> None: ...
