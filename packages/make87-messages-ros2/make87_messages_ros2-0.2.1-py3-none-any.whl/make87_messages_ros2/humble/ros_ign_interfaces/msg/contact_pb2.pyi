from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from make87_messages_ros2.humble.ros_gz_interfaces.msg import entity_pb2 as _entity_pb2
from make87_messages_ros2.humble.ros_gz_interfaces.msg import joint_wrench_pb2 as _joint_wrench_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Contact(_message.Message):
    __slots__ = ["header", "collision1", "collision2", "positions", "normals", "depths", "wrenches"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    COLLISION1_FIELD_NUMBER: _ClassVar[int]
    COLLISION2_FIELD_NUMBER: _ClassVar[int]
    POSITIONS_FIELD_NUMBER: _ClassVar[int]
    NORMALS_FIELD_NUMBER: _ClassVar[int]
    DEPTHS_FIELD_NUMBER: _ClassVar[int]
    WRENCHES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    collision1: _entity_pb2.Entity
    collision2: _entity_pb2.Entity
    positions: _containers.RepeatedCompositeFieldContainer[_vector3_pb2.Vector3]
    normals: _containers.RepeatedCompositeFieldContainer[_vector3_pb2.Vector3]
    depths: _containers.RepeatedScalarFieldContainer[float]
    wrenches: _containers.RepeatedCompositeFieldContainer[_joint_wrench_pb2.JointWrench]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., collision1: _Optional[_Union[_entity_pb2.Entity, _Mapping]] = ..., collision2: _Optional[_Union[_entity_pb2.Entity, _Mapping]] = ..., positions: _Optional[_Iterable[_Union[_vector3_pb2.Vector3, _Mapping]]] = ..., normals: _Optional[_Iterable[_Union[_vector3_pb2.Vector3, _Mapping]]] = ..., depths: _Optional[_Iterable[float]] = ..., wrenches: _Optional[_Iterable[_Union[_joint_wrench_pb2.JointWrench, _Mapping]]] = ...) -> None: ...
