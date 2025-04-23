from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rmf_traffic_msgs.msg import schedule_query_participants_pb2 as _schedule_query_participants_pb2
from make87_messages_ros2.humble.rmf_traffic_msgs.msg import schedule_query_spacetime_pb2 as _schedule_query_spacetime_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ScheduleQuery(_message.Message):
    __slots__ = ["header", "spacetime", "participants"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SPACETIME_FIELD_NUMBER: _ClassVar[int]
    PARTICIPANTS_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    spacetime: _schedule_query_spacetime_pb2.ScheduleQuerySpacetime
    participants: _schedule_query_participants_pb2.ScheduleQueryParticipants
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., spacetime: _Optional[_Union[_schedule_query_spacetime_pb2.ScheduleQuerySpacetime, _Mapping]] = ..., participants: _Optional[_Union[_schedule_query_participants_pb2.ScheduleQueryParticipants, _Mapping]] = ...) -> None: ...
