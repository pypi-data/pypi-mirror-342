from make87_messages_ros2.rolling.builtin_interfaces.msg import duration_pb2 as _duration_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BidNotice(_message.Message):
    __slots__ = ["request", "task_id", "time_window"]
    REQUEST_FIELD_NUMBER: _ClassVar[int]
    TASK_ID_FIELD_NUMBER: _ClassVar[int]
    TIME_WINDOW_FIELD_NUMBER: _ClassVar[int]
    request: str
    task_id: str
    time_window: _duration_pb2.Duration
    def __init__(self, request: _Optional[str] = ..., task_id: _Optional[str] = ..., time_window: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...) -> None: ...
