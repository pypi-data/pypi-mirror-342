from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rmf_task_msgs.msg import dispatch_state_pb2 as _dispatch_state_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DispatchStates(_message.Message):
    __slots__ = ["header", "active", "finished"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    FINISHED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    active: _containers.RepeatedCompositeFieldContainer[_dispatch_state_pb2.DispatchState]
    finished: _containers.RepeatedCompositeFieldContainer[_dispatch_state_pb2.DispatchState]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., active: _Optional[_Iterable[_Union[_dispatch_state_pb2.DispatchState, _Mapping]]] = ..., finished: _Optional[_Iterable[_Union[_dispatch_state_pb2.DispatchState, _Mapping]]] = ...) -> None: ...
