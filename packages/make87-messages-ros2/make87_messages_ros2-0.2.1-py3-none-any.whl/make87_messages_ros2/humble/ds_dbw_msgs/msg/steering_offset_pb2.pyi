from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SteeringOffset(_message.Message):
    __slots__ = ["header", "ros2_header", "steering_wheel_angle", "steering_wheel_angle_raw", "steering_wheel_angle_offset", "offset_type"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    STEERING_WHEEL_ANGLE_FIELD_NUMBER: _ClassVar[int]
    STEERING_WHEEL_ANGLE_RAW_FIELD_NUMBER: _ClassVar[int]
    STEERING_WHEEL_ANGLE_OFFSET_FIELD_NUMBER: _ClassVar[int]
    OFFSET_TYPE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    steering_wheel_angle: float
    steering_wheel_angle_raw: float
    steering_wheel_angle_offset: float
    offset_type: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., steering_wheel_angle: _Optional[float] = ..., steering_wheel_angle_raw: _Optional[float] = ..., steering_wheel_angle_offset: _Optional[float] = ..., offset_type: _Optional[int] = ...) -> None: ...
