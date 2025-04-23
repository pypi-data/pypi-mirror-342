from make87_messages_ros2.rolling.rc_reason_msgs.msg import box_pb2 as _box_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RangeBox(_message.Message):
    __slots__ = ["min_dimensions", "max_dimensions"]
    MIN_DIMENSIONS_FIELD_NUMBER: _ClassVar[int]
    MAX_DIMENSIONS_FIELD_NUMBER: _ClassVar[int]
    min_dimensions: _box_pb2.Box
    max_dimensions: _box_pb2.Box
    def __init__(self, min_dimensions: _Optional[_Union[_box_pb2.Box, _Mapping]] = ..., max_dimensions: _Optional[_Union[_box_pb2.Box, _Mapping]] = ...) -> None: ...
