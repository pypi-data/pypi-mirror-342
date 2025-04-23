from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.moveit_msgs.msg import attached_collision_object_pb2 as _attached_collision_object_pb2
from make87_messages_ros2.humble.sensor_msgs.msg import joint_state_pb2 as _joint_state_pb2
from make87_messages_ros2.humble.sensor_msgs.msg import multi_dof_joint_state_pb2 as _multi_dof_joint_state_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RobotState(_message.Message):
    __slots__ = ["header", "joint_state", "multi_dof_joint_state", "attached_collision_objects", "is_diff"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    JOINT_STATE_FIELD_NUMBER: _ClassVar[int]
    MULTI_DOF_JOINT_STATE_FIELD_NUMBER: _ClassVar[int]
    ATTACHED_COLLISION_OBJECTS_FIELD_NUMBER: _ClassVar[int]
    IS_DIFF_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    joint_state: _joint_state_pb2.JointState
    multi_dof_joint_state: _multi_dof_joint_state_pb2.MultiDOFJointState
    attached_collision_objects: _containers.RepeatedCompositeFieldContainer[_attached_collision_object_pb2.AttachedCollisionObject]
    is_diff: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., joint_state: _Optional[_Union[_joint_state_pb2.JointState, _Mapping]] = ..., multi_dof_joint_state: _Optional[_Union[_multi_dof_joint_state_pb2.MultiDOFJointState, _Mapping]] = ..., attached_collision_objects: _Optional[_Iterable[_Union[_attached_collision_object_pb2.AttachedCollisionObject, _Mapping]]] = ..., is_diff: bool = ...) -> None: ...
