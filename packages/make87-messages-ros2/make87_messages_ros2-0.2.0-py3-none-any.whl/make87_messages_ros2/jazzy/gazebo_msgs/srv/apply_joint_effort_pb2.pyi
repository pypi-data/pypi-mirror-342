from make87_messages_ros2.jazzy.builtin_interfaces.msg import duration_pb2 as _duration_pb2
from make87_messages_ros2.jazzy.builtin_interfaces.msg import time_pb2 as _time_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ApplyJointEffortRequest(_message.Message):
    __slots__ = ["joint_name", "effort", "start_time", "duration"]
    JOINT_NAME_FIELD_NUMBER: _ClassVar[int]
    EFFORT_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    DURATION_FIELD_NUMBER: _ClassVar[int]
    joint_name: str
    effort: float
    start_time: _time_pb2.Time
    duration: _duration_pb2.Duration
    def __init__(self, joint_name: _Optional[str] = ..., effort: _Optional[float] = ..., start_time: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., duration: _Optional[_Union[_duration_pb2.Duration, _Mapping]] = ...) -> None: ...

class ApplyJointEffortResponse(_message.Message):
    __slots__ = ["success", "status_message"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    STATUS_MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    status_message: str
    def __init__(self, success: bool = ..., status_message: _Optional[str] = ...) -> None: ...
