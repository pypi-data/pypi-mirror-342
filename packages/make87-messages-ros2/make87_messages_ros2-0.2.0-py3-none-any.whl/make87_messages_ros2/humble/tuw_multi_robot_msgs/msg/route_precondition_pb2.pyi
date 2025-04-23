from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RoutePrecondition(_message.Message):
    __slots__ = ["header", "robot_id", "current_route_segment"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROBOT_ID_FIELD_NUMBER: _ClassVar[int]
    CURRENT_ROUTE_SEGMENT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    robot_id: str
    current_route_segment: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., robot_id: _Optional[str] = ..., current_route_segment: _Optional[int] = ...) -> None: ...
