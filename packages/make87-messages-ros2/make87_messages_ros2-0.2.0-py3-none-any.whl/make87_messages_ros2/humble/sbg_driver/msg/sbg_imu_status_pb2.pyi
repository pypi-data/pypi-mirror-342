from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SbgImuStatus(_message.Message):
    __slots__ = ["header", "imu_com", "imu_status", "imu_accel_x", "imu_accel_y", "imu_accel_z", "imu_gyro_x", "imu_gyro_y", "imu_gyro_z", "imu_accels_in_range", "imu_gyros_in_range"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    IMU_COM_FIELD_NUMBER: _ClassVar[int]
    IMU_STATUS_FIELD_NUMBER: _ClassVar[int]
    IMU_ACCEL_X_FIELD_NUMBER: _ClassVar[int]
    IMU_ACCEL_Y_FIELD_NUMBER: _ClassVar[int]
    IMU_ACCEL_Z_FIELD_NUMBER: _ClassVar[int]
    IMU_GYRO_X_FIELD_NUMBER: _ClassVar[int]
    IMU_GYRO_Y_FIELD_NUMBER: _ClassVar[int]
    IMU_GYRO_Z_FIELD_NUMBER: _ClassVar[int]
    IMU_ACCELS_IN_RANGE_FIELD_NUMBER: _ClassVar[int]
    IMU_GYROS_IN_RANGE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    imu_com: bool
    imu_status: bool
    imu_accel_x: bool
    imu_accel_y: bool
    imu_accel_z: bool
    imu_gyro_x: bool
    imu_gyro_y: bool
    imu_gyro_z: bool
    imu_accels_in_range: bool
    imu_gyros_in_range: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., imu_com: bool = ..., imu_status: bool = ..., imu_accel_x: bool = ..., imu_accel_y: bool = ..., imu_accel_z: bool = ..., imu_gyro_x: bool = ..., imu_gyro_y: bool = ..., imu_gyro_z: bool = ..., imu_accels_in_range: bool = ..., imu_gyros_in_range: bool = ...) -> None: ...
