from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class WaypointReached(_message.Message):
    __slots__ = ["header", "wp_seq"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    WP_SEQ_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    wp_seq: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., wp_seq: _Optional[int] = ...) -> None: ...
