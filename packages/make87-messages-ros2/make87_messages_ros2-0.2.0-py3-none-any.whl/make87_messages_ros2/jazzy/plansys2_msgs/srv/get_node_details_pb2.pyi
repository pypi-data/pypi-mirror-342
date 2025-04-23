from make87_messages_ros2.jazzy.plansys2_msgs.msg import node_pb2 as _node_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GetNodeDetailsRequest(_message.Message):
    __slots__ = ["expression"]
    EXPRESSION_FIELD_NUMBER: _ClassVar[int]
    expression: str
    def __init__(self, expression: _Optional[str] = ...) -> None: ...

class GetNodeDetailsResponse(_message.Message):
    __slots__ = ["success", "node", "error_info"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    NODE_FIELD_NUMBER: _ClassVar[int]
    ERROR_INFO_FIELD_NUMBER: _ClassVar[int]
    success: bool
    node: _node_pb2.Node
    error_info: str
    def __init__(self, success: bool = ..., node: _Optional[_Union[_node_pb2.Node, _Mapping]] = ..., error_info: _Optional[str] = ...) -> None: ...
