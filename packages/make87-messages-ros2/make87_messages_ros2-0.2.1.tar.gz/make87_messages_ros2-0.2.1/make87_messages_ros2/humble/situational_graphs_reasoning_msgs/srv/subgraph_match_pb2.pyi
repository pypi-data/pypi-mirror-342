from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.situational_graphs_reasoning_msgs.msg import graph_pb2 as _graph_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SubgraphMatchRequest(_message.Message):
    __slots__ = ["header", "base_graph", "target_graph"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    BASE_GRAPH_FIELD_NUMBER: _ClassVar[int]
    TARGET_GRAPH_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    base_graph: str
    target_graph: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., base_graph: _Optional[str] = ..., target_graph: _Optional[str] = ...) -> None: ...

class SubgraphMatchResponse(_message.Message):
    __slots__ = ["header", "success", "matches", "score"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MATCHES_FIELD_NUMBER: _ClassVar[int]
    SCORE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: int
    matches: _containers.RepeatedCompositeFieldContainer[_graph_pb2.Graph]
    score: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: _Optional[int] = ..., matches: _Optional[_Iterable[_Union[_graph_pb2.Graph, _Mapping]]] = ..., score: _Optional[_Iterable[float]] = ...) -> None: ...
