from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rmf_scheduler_msgs.msg import trigger_pb2 as _trigger_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ListTriggersRequest(_message.Message):
    __slots__ = ["header", "created_after"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CREATED_AFTER_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    created_after: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., created_after: _Optional[int] = ...) -> None: ...

class ListTriggersResponse(_message.Message):
    __slots__ = ["header", "success", "message", "triggers"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    TRIGGERS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    message: str
    triggers: _containers.RepeatedCompositeFieldContainer[_trigger_pb2.Trigger]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., message: _Optional[str] = ..., triggers: _Optional[_Iterable[_Union[_trigger_pb2.Trigger, _Mapping]]] = ...) -> None: ...
