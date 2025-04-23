from make87_messages_ros2.jazzy.plansys2_msgs.msg import node_pb2 as _node_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class AffectNodeRequest(_message.Message):
    __slots__ = ["node"]
    NODE_FIELD_NUMBER: _ClassVar[int]
    node: _node_pb2.Node
    def __init__(self, node: _Optional[_Union[_node_pb2.Node, _Mapping]] = ...) -> None: ...

class AffectNodeResponse(_message.Message):
    __slots__ = ["success", "error_info"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    ERROR_INFO_FIELD_NUMBER: _ClassVar[int]
    success: bool
    error_info: str
    def __init__(self, success: bool = ..., error_info: _Optional[str] = ...) -> None: ...
