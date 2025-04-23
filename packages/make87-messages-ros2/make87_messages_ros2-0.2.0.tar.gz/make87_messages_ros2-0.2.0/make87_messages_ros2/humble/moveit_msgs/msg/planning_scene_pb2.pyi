from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import transform_stamped_pb2 as _transform_stamped_pb2
from make87_messages_ros2.humble.moveit_msgs.msg import allowed_collision_matrix_pb2 as _allowed_collision_matrix_pb2
from make87_messages_ros2.humble.moveit_msgs.msg import link_padding_pb2 as _link_padding_pb2
from make87_messages_ros2.humble.moveit_msgs.msg import link_scale_pb2 as _link_scale_pb2
from make87_messages_ros2.humble.moveit_msgs.msg import object_color_pb2 as _object_color_pb2
from make87_messages_ros2.humble.moveit_msgs.msg import planning_scene_world_pb2 as _planning_scene_world_pb2
from make87_messages_ros2.humble.moveit_msgs.msg import robot_state_pb2 as _robot_state_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class PlanningScene(_message.Message):
    __slots__ = ["header", "name", "robot_state", "robot_model_name", "fixed_frame_transforms", "allowed_collision_matrix", "link_padding", "link_scale", "object_colors", "world", "is_diff"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ROBOT_STATE_FIELD_NUMBER: _ClassVar[int]
    ROBOT_MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    FIXED_FRAME_TRANSFORMS_FIELD_NUMBER: _ClassVar[int]
    ALLOWED_COLLISION_MATRIX_FIELD_NUMBER: _ClassVar[int]
    LINK_PADDING_FIELD_NUMBER: _ClassVar[int]
    LINK_SCALE_FIELD_NUMBER: _ClassVar[int]
    OBJECT_COLORS_FIELD_NUMBER: _ClassVar[int]
    WORLD_FIELD_NUMBER: _ClassVar[int]
    IS_DIFF_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    name: str
    robot_state: _robot_state_pb2.RobotState
    robot_model_name: str
    fixed_frame_transforms: _containers.RepeatedCompositeFieldContainer[_transform_stamped_pb2.TransformStamped]
    allowed_collision_matrix: _allowed_collision_matrix_pb2.AllowedCollisionMatrix
    link_padding: _containers.RepeatedCompositeFieldContainer[_link_padding_pb2.LinkPadding]
    link_scale: _containers.RepeatedCompositeFieldContainer[_link_scale_pb2.LinkScale]
    object_colors: _containers.RepeatedCompositeFieldContainer[_object_color_pb2.ObjectColor]
    world: _planning_scene_world_pb2.PlanningSceneWorld
    is_diff: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., name: _Optional[str] = ..., robot_state: _Optional[_Union[_robot_state_pb2.RobotState, _Mapping]] = ..., robot_model_name: _Optional[str] = ..., fixed_frame_transforms: _Optional[_Iterable[_Union[_transform_stamped_pb2.TransformStamped, _Mapping]]] = ..., allowed_collision_matrix: _Optional[_Union[_allowed_collision_matrix_pb2.AllowedCollisionMatrix, _Mapping]] = ..., link_padding: _Optional[_Iterable[_Union[_link_padding_pb2.LinkPadding, _Mapping]]] = ..., link_scale: _Optional[_Iterable[_Union[_link_scale_pb2.LinkScale, _Mapping]]] = ..., object_colors: _Optional[_Iterable[_Union[_object_color_pb2.ObjectColor, _Mapping]]] = ..., world: _Optional[_Union[_planning_scene_world_pb2.PlanningSceneWorld, _Mapping]] = ..., is_diff: bool = ...) -> None: ...
