from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.puma_motor_msgs.msg import feedback_pb2 as _feedback_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MultiFeedback(_message.Message):
    __slots__ = ["header", "ros2_header", "drivers_feedback"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    DRIVERS_FEEDBACK_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    drivers_feedback: _containers.RepeatedCompositeFieldContainer[_feedback_pb2.Feedback]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., drivers_feedback: _Optional[_Iterable[_Union[_feedback_pb2.Feedback, _Mapping]]] = ...) -> None: ...
