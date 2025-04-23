from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EyeTracker(_message.Message):
    __slots__ = ["header", "ros2_header", "attention", "gaze", "eyes_present"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    ATTENTION_FIELD_NUMBER: _ClassVar[int]
    GAZE_FIELD_NUMBER: _ClassVar[int]
    EYES_PRESENT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    attention: float
    gaze: int
    eyes_present: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., attention: _Optional[float] = ..., gaze: _Optional[int] = ..., eyes_present: bool = ...) -> None: ...
