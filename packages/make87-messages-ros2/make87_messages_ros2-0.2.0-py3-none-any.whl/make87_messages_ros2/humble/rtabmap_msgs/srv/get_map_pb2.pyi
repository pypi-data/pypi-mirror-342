from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rtabmap_msgs.msg import map_data_pb2 as _map_data_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetMapRequest(_message.Message):
    __slots__ = ["header", "global_map", "optimized", "graph_only"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    GLOBAL_MAP_FIELD_NUMBER: _ClassVar[int]
    OPTIMIZED_FIELD_NUMBER: _ClassVar[int]
    GRAPH_ONLY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    global_map: bool
    optimized: bool
    graph_only: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., global_map: bool = ..., optimized: bool = ..., graph_only: bool = ...) -> None: ...

class GetMapResponse(_message.Message):
    __slots__ = ["header", "data"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    data: _map_data_pb2.MapData
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., data: _Optional[_Union[_map_data_pb2.MapData, _Mapping]] = ...) -> None: ...
