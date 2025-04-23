from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.sensor_msgs.msg import imu_pb2 as _imu_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ImuExtended(_message.Message):
    __slots__ = ["header", "ros2_header", "imu", "ticks", "quaternion_accuracy", "angular_velocity_reliability", "linear_acceleration_reliability"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    IMU_FIELD_NUMBER: _ClassVar[int]
    TICKS_FIELD_NUMBER: _ClassVar[int]
    QUATERNION_ACCURACY_FIELD_NUMBER: _ClassVar[int]
    ANGULAR_VELOCITY_RELIABILITY_FIELD_NUMBER: _ClassVar[int]
    LINEAR_ACCELERATION_RELIABILITY_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    imu: _imu_pb2.Imu
    ticks: int
    quaternion_accuracy: float
    angular_velocity_reliability: int
    linear_acceleration_reliability: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., imu: _Optional[_Union[_imu_pb2.Imu, _Mapping]] = ..., ticks: _Optional[int] = ..., quaternion_accuracy: _Optional[float] = ..., angular_velocity_reliability: _Optional[int] = ..., linear_acceleration_reliability: _Optional[int] = ...) -> None: ...
