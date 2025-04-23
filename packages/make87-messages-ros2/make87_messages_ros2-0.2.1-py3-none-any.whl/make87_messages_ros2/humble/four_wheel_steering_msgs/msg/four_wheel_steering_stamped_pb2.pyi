from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.four_wheel_steering_msgs.msg import four_wheel_steering_pb2 as _four_wheel_steering_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class FourWheelSteeringStamped(_message.Message):
    __slots__ = ["header", "ros2_header", "data"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    data: _four_wheel_steering_pb2.FourWheelSteering
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., data: _Optional[_Union[_four_wheel_steering_pb2.FourWheelSteering, _Mapping]] = ...) -> None: ...
