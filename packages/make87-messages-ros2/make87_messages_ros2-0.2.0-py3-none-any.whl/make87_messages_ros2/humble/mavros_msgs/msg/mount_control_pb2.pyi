from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MountControl(_message.Message):
    __slots__ = ["header", "ros2_header", "mode", "pitch", "roll", "yaw", "altitude", "latitude", "longitude"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    PITCH_FIELD_NUMBER: _ClassVar[int]
    ROLL_FIELD_NUMBER: _ClassVar[int]
    YAW_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    mode: int
    pitch: float
    roll: float
    yaw: float
    altitude: float
    latitude: float
    longitude: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., mode: _Optional[int] = ..., pitch: _Optional[float] = ..., roll: _Optional[float] = ..., yaw: _Optional[float] = ..., altitude: _Optional[float] = ..., latitude: _Optional[float] = ..., longitude: _Optional[float] = ...) -> None: ...
