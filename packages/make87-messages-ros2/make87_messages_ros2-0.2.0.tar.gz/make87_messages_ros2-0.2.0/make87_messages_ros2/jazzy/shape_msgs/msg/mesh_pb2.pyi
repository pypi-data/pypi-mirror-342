from make87_messages_ros2.jazzy.geometry_msgs.msg import point_pb2 as _point_pb2
from make87_messages_ros2.jazzy.shape_msgs.msg import mesh_triangle_pb2 as _mesh_triangle_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Mesh(_message.Message):
    __slots__ = ["triangles", "vertices"]
    TRIANGLES_FIELD_NUMBER: _ClassVar[int]
    VERTICES_FIELD_NUMBER: _ClassVar[int]
    triangles: _containers.RepeatedCompositeFieldContainer[_mesh_triangle_pb2.MeshTriangle]
    vertices: _containers.RepeatedCompositeFieldContainer[_point_pb2.Point]
    def __init__(self, triangles: _Optional[_Iterable[_Union[_mesh_triangle_pb2.MeshTriangle, _Mapping]]] = ..., vertices: _Optional[_Iterable[_Union[_point_pb2.Point, _Mapping]]] = ...) -> None: ...
