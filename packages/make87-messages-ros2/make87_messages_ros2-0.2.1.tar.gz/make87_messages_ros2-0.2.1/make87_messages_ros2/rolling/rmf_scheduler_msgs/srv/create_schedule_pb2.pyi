from make87_messages_ros2.rolling.rmf_scheduler_msgs.msg import schedule_pb2 as _schedule_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateScheduleRequest(_message.Message):
    __slots__ = ["schedule"]
    SCHEDULE_FIELD_NUMBER: _ClassVar[int]
    schedule: _schedule_pb2.Schedule
    def __init__(self, schedule: _Optional[_Union[_schedule_pb2.Schedule, _Mapping]] = ...) -> None: ...

class CreateScheduleResponse(_message.Message):
    __slots__ = ["success", "message"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    success: bool
    message: str
    def __init__(self, success: bool = ..., message: _Optional[str] = ...) -> None: ...
