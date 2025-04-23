from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class NavControllerOutput(_message.Message):
    __slots__ = ["header", "ros2_header", "nav_roll", "nav_pitch", "nav_bearing", "target_bearing", "wp_dist", "alt_error", "aspd_error", "xtrack_error"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    NAV_ROLL_FIELD_NUMBER: _ClassVar[int]
    NAV_PITCH_FIELD_NUMBER: _ClassVar[int]
    NAV_BEARING_FIELD_NUMBER: _ClassVar[int]
    TARGET_BEARING_FIELD_NUMBER: _ClassVar[int]
    WP_DIST_FIELD_NUMBER: _ClassVar[int]
    ALT_ERROR_FIELD_NUMBER: _ClassVar[int]
    ASPD_ERROR_FIELD_NUMBER: _ClassVar[int]
    XTRACK_ERROR_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    nav_roll: float
    nav_pitch: float
    nav_bearing: int
    target_bearing: int
    wp_dist: int
    alt_error: float
    aspd_error: float
    xtrack_error: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., nav_roll: _Optional[float] = ..., nav_pitch: _Optional[float] = ..., nav_bearing: _Optional[int] = ..., target_bearing: _Optional[int] = ..., wp_dist: _Optional[int] = ..., alt_error: _Optional[float] = ..., aspd_error: _Optional[float] = ..., xtrack_error: _Optional[float] = ...) -> None: ...
