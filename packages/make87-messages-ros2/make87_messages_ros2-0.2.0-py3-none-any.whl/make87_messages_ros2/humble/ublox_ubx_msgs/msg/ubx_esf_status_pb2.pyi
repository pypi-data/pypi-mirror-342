from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from make87_messages_ros2.humble.ublox_ubx_msgs.msg import esf_sensor_status_pb2 as _esf_sensor_status_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UBXEsfStatus(_message.Message):
    __slots__ = ["header", "ros2_header", "itow", "version", "wt_init_status", "mnt_alg_status", "ins_init_status", "imu_init_status", "fusion_mode", "num_sens", "sensor_statuses"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    ITOW_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    WT_INIT_STATUS_FIELD_NUMBER: _ClassVar[int]
    MNT_ALG_STATUS_FIELD_NUMBER: _ClassVar[int]
    INS_INIT_STATUS_FIELD_NUMBER: _ClassVar[int]
    IMU_INIT_STATUS_FIELD_NUMBER: _ClassVar[int]
    FUSION_MODE_FIELD_NUMBER: _ClassVar[int]
    NUM_SENS_FIELD_NUMBER: _ClassVar[int]
    SENSOR_STATUSES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    itow: int
    version: int
    wt_init_status: int
    mnt_alg_status: int
    ins_init_status: int
    imu_init_status: int
    fusion_mode: int
    num_sens: int
    sensor_statuses: _containers.RepeatedCompositeFieldContainer[_esf_sensor_status_pb2.ESFSensorStatus]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., itow: _Optional[int] = ..., version: _Optional[int] = ..., wt_init_status: _Optional[int] = ..., mnt_alg_status: _Optional[int] = ..., ins_init_status: _Optional[int] = ..., imu_init_status: _Optional[int] = ..., fusion_mode: _Optional[int] = ..., num_sens: _Optional[int] = ..., sensor_statuses: _Optional[_Iterable[_Union[_esf_sensor_status_pb2.ESFSensorStatus, _Mapping]]] = ...) -> None: ...
