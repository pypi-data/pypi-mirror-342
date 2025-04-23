from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.off_highway_premium_radar_sample_msgs.msg import sensor_broadcast_data_pb2 as _sensor_broadcast_data_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SensorBroadcast(_message.Message):
    __slots__ = ["header", "ros2_header", "lgp_version", "sensor_broadcast_data"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    LGP_VERSION_FIELD_NUMBER: _ClassVar[int]
    SENSOR_BROADCAST_DATA_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    lgp_version: int
    sensor_broadcast_data: _sensor_broadcast_data_pb2.SensorBroadcastData
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., lgp_version: _Optional[int] = ..., sensor_broadcast_data: _Optional[_Union[_sensor_broadcast_data_pb2.SensorBroadcastData, _Mapping]] = ...) -> None: ...
