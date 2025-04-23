from make87_messages_ros2.jazzy.geometry_msgs.msg import point_pb2 as _point_pb2
from make87_messages_ros2.jazzy.graph_msgs.msg import edges_pb2 as _edges_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GeometryGraph(_message.Message):
    __slots__ = ["header", "nodes", "edges"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NODES_FIELD_NUMBER: _ClassVar[int]
    EDGES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    nodes: _containers.RepeatedCompositeFieldContainer[_point_pb2.Point]
    edges: _containers.RepeatedCompositeFieldContainer[_edges_pb2.Edges]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., nodes: _Optional[_Iterable[_Union[_point_pb2.Point, _Mapping]]] = ..., edges: _Optional[_Iterable[_Union[_edges_pb2.Edges, _Mapping]]] = ...) -> None: ...
