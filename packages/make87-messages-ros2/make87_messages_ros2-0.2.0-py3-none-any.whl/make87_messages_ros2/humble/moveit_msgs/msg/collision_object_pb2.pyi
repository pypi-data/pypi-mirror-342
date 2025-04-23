from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.humble.object_recognition_msgs.msg import object_type_pb2 as _object_type_pb2
from make87_messages_ros2.humble.shape_msgs.msg import mesh_pb2 as _mesh_pb2
from make87_messages_ros2.humble.shape_msgs.msg import plane_pb2 as _plane_pb2
from make87_messages_ros2.humble.shape_msgs.msg import solid_primitive_pb2 as _solid_primitive_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CollisionObject(_message.Message):
    __slots__ = ["header", "ros2_header", "pose", "id", "type", "primitives", "primitive_poses", "meshes", "mesh_poses", "planes", "plane_poses", "subframe_names", "subframe_poses", "operation"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    POSE_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    PRIMITIVES_FIELD_NUMBER: _ClassVar[int]
    PRIMITIVE_POSES_FIELD_NUMBER: _ClassVar[int]
    MESHES_FIELD_NUMBER: _ClassVar[int]
    MESH_POSES_FIELD_NUMBER: _ClassVar[int]
    PLANES_FIELD_NUMBER: _ClassVar[int]
    PLANE_POSES_FIELD_NUMBER: _ClassVar[int]
    SUBFRAME_NAMES_FIELD_NUMBER: _ClassVar[int]
    SUBFRAME_POSES_FIELD_NUMBER: _ClassVar[int]
    OPERATION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    pose: _pose_pb2.Pose
    id: str
    type: _object_type_pb2.ObjectType
    primitives: _containers.RepeatedCompositeFieldContainer[_solid_primitive_pb2.SolidPrimitive]
    primitive_poses: _containers.RepeatedCompositeFieldContainer[_pose_pb2.Pose]
    meshes: _containers.RepeatedCompositeFieldContainer[_mesh_pb2.Mesh]
    mesh_poses: _containers.RepeatedCompositeFieldContainer[_pose_pb2.Pose]
    planes: _containers.RepeatedCompositeFieldContainer[_plane_pb2.Plane]
    plane_poses: _containers.RepeatedCompositeFieldContainer[_pose_pb2.Pose]
    subframe_names: _containers.RepeatedScalarFieldContainer[str]
    subframe_poses: _containers.RepeatedCompositeFieldContainer[_pose_pb2.Pose]
    operation: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., pose: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., id: _Optional[str] = ..., type: _Optional[_Union[_object_type_pb2.ObjectType, _Mapping]] = ..., primitives: _Optional[_Iterable[_Union[_solid_primitive_pb2.SolidPrimitive, _Mapping]]] = ..., primitive_poses: _Optional[_Iterable[_Union[_pose_pb2.Pose, _Mapping]]] = ..., meshes: _Optional[_Iterable[_Union[_mesh_pb2.Mesh, _Mapping]]] = ..., mesh_poses: _Optional[_Iterable[_Union[_pose_pb2.Pose, _Mapping]]] = ..., planes: _Optional[_Iterable[_Union[_plane_pb2.Plane, _Mapping]]] = ..., plane_poses: _Optional[_Iterable[_Union[_pose_pb2.Pose, _Mapping]]] = ..., subframe_names: _Optional[_Iterable[str]] = ..., subframe_poses: _Optional[_Iterable[_Union[_pose_pb2.Pose, _Mapping]]] = ..., operation: _Optional[int] = ...) -> None: ...
