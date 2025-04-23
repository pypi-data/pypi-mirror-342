from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.plansys2_msgs.msg import param_pb2 as _param_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Node(_message.Message):
    __slots__ = ["header", "node_type", "expression_type", "modifier_type", "node_id", "children", "name", "parameters", "value", "negate"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NODE_TYPE_FIELD_NUMBER: _ClassVar[int]
    EXPRESSION_TYPE_FIELD_NUMBER: _ClassVar[int]
    MODIFIER_TYPE_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    CHILDREN_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PARAMETERS_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    NEGATE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    node_type: int
    expression_type: int
    modifier_type: int
    node_id: int
    children: _containers.RepeatedScalarFieldContainer[int]
    name: str
    parameters: _containers.RepeatedCompositeFieldContainer[_param_pb2.Param]
    value: float
    negate: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., node_type: _Optional[int] = ..., expression_type: _Optional[int] = ..., modifier_type: _Optional[int] = ..., node_id: _Optional[int] = ..., children: _Optional[_Iterable[int]] = ..., name: _Optional[str] = ..., parameters: _Optional[_Iterable[_Union[_param_pb2.Param, _Mapping]]] = ..., value: _Optional[float] = ..., negate: bool = ...) -> None: ...
