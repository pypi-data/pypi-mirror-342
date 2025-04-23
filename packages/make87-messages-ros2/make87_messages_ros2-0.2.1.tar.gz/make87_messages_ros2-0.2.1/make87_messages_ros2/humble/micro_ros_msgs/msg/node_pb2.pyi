from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.micro_ros_msgs.msg import entity_pb2 as _entity_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Node(_message.Message):
    __slots__ = ["header", "node_namespace", "node_name", "entities"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NODE_NAMESPACE_FIELD_NUMBER: _ClassVar[int]
    NODE_NAME_FIELD_NUMBER: _ClassVar[int]
    ENTITIES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    node_namespace: str
    node_name: str
    entities: _containers.RepeatedCompositeFieldContainer[_entity_pb2.Entity]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., node_namespace: _Optional[str] = ..., node_name: _Optional[str] = ..., entities: _Optional[_Iterable[_Union[_entity_pb2.Entity, _Mapping]]] = ...) -> None: ...
