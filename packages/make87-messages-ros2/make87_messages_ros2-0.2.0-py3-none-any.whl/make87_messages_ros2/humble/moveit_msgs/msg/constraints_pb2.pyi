from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.moveit_msgs.msg import joint_constraint_pb2 as _joint_constraint_pb2
from make87_messages_ros2.humble.moveit_msgs.msg import orientation_constraint_pb2 as _orientation_constraint_pb2
from make87_messages_ros2.humble.moveit_msgs.msg import position_constraint_pb2 as _position_constraint_pb2
from make87_messages_ros2.humble.moveit_msgs.msg import visibility_constraint_pb2 as _visibility_constraint_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Constraints(_message.Message):
    __slots__ = ["header", "name", "joint_constraints", "position_constraints", "orientation_constraints", "visibility_constraints"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    JOINT_CONSTRAINTS_FIELD_NUMBER: _ClassVar[int]
    POSITION_CONSTRAINTS_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_CONSTRAINTS_FIELD_NUMBER: _ClassVar[int]
    VISIBILITY_CONSTRAINTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    name: str
    joint_constraints: _containers.RepeatedCompositeFieldContainer[_joint_constraint_pb2.JointConstraint]
    position_constraints: _containers.RepeatedCompositeFieldContainer[_position_constraint_pb2.PositionConstraint]
    orientation_constraints: _containers.RepeatedCompositeFieldContainer[_orientation_constraint_pb2.OrientationConstraint]
    visibility_constraints: _containers.RepeatedCompositeFieldContainer[_visibility_constraint_pb2.VisibilityConstraint]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., name: _Optional[str] = ..., joint_constraints: _Optional[_Iterable[_Union[_joint_constraint_pb2.JointConstraint, _Mapping]]] = ..., position_constraints: _Optional[_Iterable[_Union[_position_constraint_pb2.PositionConstraint, _Mapping]]] = ..., orientation_constraints: _Optional[_Iterable[_Union[_orientation_constraint_pb2.OrientationConstraint, _Mapping]]] = ..., visibility_constraints: _Optional[_Iterable[_Union[_visibility_constraint_pb2.VisibilityConstraint, _Mapping]]] = ...) -> None: ...
