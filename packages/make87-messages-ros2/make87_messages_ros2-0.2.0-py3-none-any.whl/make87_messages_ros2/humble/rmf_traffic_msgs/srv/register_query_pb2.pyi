from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.rmf_traffic_msgs.msg import schedule_identity_pb2 as _schedule_identity_pb2
from make87_messages_ros2.humble.rmf_traffic_msgs.msg import schedule_query_pb2 as _schedule_query_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RegisterQueryRequest(_message.Message):
    __slots__ = ["header", "query"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    QUERY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    query: _schedule_query_pb2.ScheduleQuery
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., query: _Optional[_Union[_schedule_query_pb2.ScheduleQuery, _Mapping]] = ...) -> None: ...

class RegisterQueryResponse(_message.Message):
    __slots__ = ["header", "node_id", "query_id", "error"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    NODE_ID_FIELD_NUMBER: _ClassVar[int]
    QUERY_ID_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    node_id: _schedule_identity_pb2.ScheduleIdentity
    query_id: int
    error: str
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., node_id: _Optional[_Union[_schedule_identity_pb2.ScheduleIdentity, _Mapping]] = ..., query_id: _Optional[int] = ..., error: _Optional[str] = ...) -> None: ...
