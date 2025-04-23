from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.builtin_interfaces.msg import time_pb2 as _time_pb2
from make87_messages_ros2.humble.nav2_msgs.msg import behavior_tree_status_change_pb2 as _behavior_tree_status_change_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class BehaviorTreeLog(_message.Message):
    __slots__ = ["header", "timestamp", "event_log"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    EVENT_LOG_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    timestamp: _time_pb2.Time
    event_log: _containers.RepeatedCompositeFieldContainer[_behavior_tree_status_change_pb2.BehaviorTreeStatusChange]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., timestamp: _Optional[_Union[_time_pb2.Time, _Mapping]] = ..., event_log: _Optional[_Iterable[_Union[_behavior_tree_status_change_pb2.BehaviorTreeStatusChange, _Mapping]]] = ...) -> None: ...
