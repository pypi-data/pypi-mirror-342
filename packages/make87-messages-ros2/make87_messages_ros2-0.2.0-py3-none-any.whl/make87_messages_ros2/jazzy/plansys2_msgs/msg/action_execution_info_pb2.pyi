from make87_messages_ros2.jazzy.builtin_interfaces.msg import duration_pb2 as _duration_pb2
from make87_messages_ros2.jazzy.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ActionExecutionInfo(_message.Message):
    __slots__ = ["status", "start_stamp", "status_stamp", "action_full_name", "action", "arguments", "duration", "completion", "message_status"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    START_STAMP_FIELD_NUMBER: _ClassVar[int]
    STATUS_STAMP_FIELD_NUMBER: _ClassVar[int]
    ACTION_FULL_NAME_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    ARGUMENTS_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    COMPLETION_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_STATUS_FIELD_NUMBER: _ClassVar[int]
    status: int
    start_stamp: _time_pb2.Time
    status_stamp: _time_pb2.Time
    action_full_name: str
    action: str
    arguments: _containers.RepeatedScalarFieldContainer[str]
    duration: _duration_pb2.Duration
    completion: float
    message_status: str
    def __init__(self, status: _Optional[int] = ..., start_stamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., status_stamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., action_full_name: _Optional[str] = ..., action: _Optional[str] = ..., arguments: _Optional[_Iterable[str]] = ..., duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ..., completion: _Optional[float] = ..., message_status: _Optional[str] = ...) -> None: ...
