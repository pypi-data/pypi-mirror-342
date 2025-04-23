from make87_messages_ros2.rolling.geometry_msgs.msg import pose_pb2 as _pose_pb2
from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from make87_messages_ros2.rolling.tuw_graph_msgs.msg import edge_pb2 as _edge_pb2
from make87_messages_ros2.rolling.tuw_graph_msgs.msg import node_pb2 as _node_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Graph(_message.Message):
    __slots__ = ["header", "origin", "nodes", "edges"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    NODES_FIELD_NUMBER: _ClassVar[int]
    EDGES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    origin: _pose_pb2.Pose
    nodes: _containers.RepeatedCompositeFieldContainer[_node_pb2.Node]
    edges: _containers.RepeatedCompositeFieldContainer[_edge_pb2.Edge]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., origin: _Optional[_Union[_pose_pb2.Pose, _Mapping]] = ..., nodes: _Optional[_Iterable[_Union[_node_pb2.Node, _Mapping]]] = ..., edges: _Optional[_Iterable[_Union[_edge_pb2.Edge, _Mapping]]] = ...) -> None: ...
