from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.robot_controllers_msgs.msg import controller_state_pb2 as _controller_state_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class QueryControllerStatesRequest(_message.Message):
    __slots__ = ["header", "updates"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    UPDATES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    updates: _containers.RepeatedCompositeFieldContainer[_controller_state_pb2.ControllerState]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., updates: _Optional[_Iterable[_Union[_controller_state_pb2.ControllerState, _Mapping]]] = ...) -> None: ...

class QueryControllerStatesResponse(_message.Message):
    __slots__ = ["header", "state"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    state: _containers.RepeatedCompositeFieldContainer[_controller_state_pb2.ControllerState]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., state: _Optional[_Iterable[_Union[_controller_state_pb2.ControllerState, _Mapping]]] = ...) -> None: ...
