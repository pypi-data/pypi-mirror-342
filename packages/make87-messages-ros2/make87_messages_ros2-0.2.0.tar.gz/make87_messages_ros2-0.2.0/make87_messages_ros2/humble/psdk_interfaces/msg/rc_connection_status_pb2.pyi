from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class RCConnectionStatus(_message.Message):
    __slots__ = ["header", "ros2_header", "air_connection", "ground_connection", "app_connection", "air_or_ground_disconnected"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    AIR_CONNECTION_FIELD_NUMBER: _ClassVar[int]
    GROUND_CONNECTION_FIELD_NUMBER: _ClassVar[int]
    APP_CONNECTION_FIELD_NUMBER: _ClassVar[int]
    AIR_OR_GROUND_DISCONNECTED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    air_connection: int
    ground_connection: int
    app_connection: int
    air_or_ground_disconnected: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., air_connection: _Optional[int] = ..., ground_connection: _Optional[int] = ..., app_connection: _Optional[int] = ..., air_or_ground_disconnected: _Optional[int] = ...) -> None: ...
