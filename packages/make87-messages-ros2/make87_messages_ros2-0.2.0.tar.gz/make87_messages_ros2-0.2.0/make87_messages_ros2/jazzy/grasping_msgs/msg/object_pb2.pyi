from make87_messages_ros2.jazzy.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.jazzy.grasping_msgs.msg import object_property_pb2 as _object_property_pb2
from make87_messages_ros2.jazzy.sensor_msgs.msg import point_cloud2_pb2 as _point_cloud2_pb2
from make87_messages_ros2.jazzy.shape_msgs.msg import mesh_pb2 as _mesh_pb2
from make87_messages_ros2.jazzy.shape_msgs.msg import plane_pb2 as _plane_pb2
from make87_messages_ros2.jazzy.shape_msgs.msg import solid_primitive_pb2 as _solid_primitive_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Object(_message.Message):
    __slots__ = ["header", "name", "support_surface", "properties", "point_cluster", "primitives", "primitive_poses", "meshes", "mesh_poses", "surface"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SUPPORT_SURFACE_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    POINT_CLUSTER_FIELD_NUMBER: _ClassVar[int]
    PRIMITIVES_FIELD_NUMBER: _ClassVar[int]
    PRIMITIVE_POSES_FIELD_NUMBER: _ClassVar[int]
    MESHES_FIELD_NUMBER: _ClassVar[int]
    MESH_POSES_FIELD_NUMBER: _ClassVar[int]
    SURFACE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    name: str
    support_surface: str
    properties: _containers.RepeatedCompositeFieldContainer[_object_property_pb2.ObjectProperty]
    point_cluster: _point_cloud2_pb2.PointCloud2
    primitives: _containers.RepeatedCompositeFieldContainer[_solid_primitive_pb2.SolidPrimitive]
    primitive_poses: _containers.RepeatedCompositeFieldContainer[_pose_pb2.Pose]
    meshes: _containers.RepeatedCompositeFieldContainer[_mesh_pb2.Mesh]
    mesh_poses: _containers.RepeatedCompositeFieldContainer[_pose_pb2.Pose]
    surface: _plane_pb2.Plane
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., name: _Optional[str] = ..., support_surface: _Optional[str] = ..., properties: _Optional[_Iterable[_Union[_object_property_pb2.ObjectProperty, _Mapping]]] = ..., point_cluster: _Optional[_Union[_point_cloud2_pb2.PointCloud2, _Mapping]] = ..., primitives: _Optional[_Iterable[_Union[_solid_primitive_pb2.SolidPrimitive, _Mapping]]] = ..., primitive_poses: _Optional[_Iterable[_Union[_pose_pb2.Pose, _Mapping]]] = ..., meshes: _Optional[_Iterable[_Union[_mesh_pb2.Mesh, _Mapping]]] = ..., mesh_poses: _Optional[_Iterable[_Union[_pose_pb2.Pose, _Mapping]]] = ..., surface: _Optional[_Union[_plane_pb2.Plane, _Mapping]] = ...) -> None: ...
