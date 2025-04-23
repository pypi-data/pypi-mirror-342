from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rmf_task_msgs.msg import task_summary_pb2 as _task_summary_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Tasks(_message.Message):
    __slots__ = ["header", "tasks"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TASKS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    tasks: _containers.RepeatedCompositeFieldContainer[_task_summary_pb2.TaskSummary]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., tasks: _Optional[_Iterable[_Union[_task_summary_pb2.TaskSummary, _Mapping]]] = ...) -> None: ...
