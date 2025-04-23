from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class VfrHud(_message.Message):
    __slots__ = ["header", "ros2_header", "airspeed", "groundspeed", "heading", "throttle", "altitude", "climb"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    AIRSPEED_FIELD_NUMBER: _ClassVar[int]
    GROUNDSPEED_FIELD_NUMBER: _ClassVar[int]
    HEADING_FIELD_NUMBER: _ClassVar[int]
    THROTTLE_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_FIELD_NUMBER: _ClassVar[int]
    CLIMB_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    airspeed: float
    groundspeed: float
    heading: int
    throttle: float
    altitude: float
    climb: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., airspeed: _Optional[float] = ..., groundspeed: _Optional[float] = ..., heading: _Optional[int] = ..., throttle: _Optional[float] = ..., altitude: _Optional[float] = ..., climb: _Optional[float] = ...) -> None: ...
