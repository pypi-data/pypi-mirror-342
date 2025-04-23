from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SetImuCalibrationRequest(_message.Message):
    __slots__ = ["gyro_bias_x", "gyro_bias_y", "gyro_bias_z"]
    GYRO_BIAS_X_FIELD_NUMBER: _ClassVar[int]
    GYRO_BIAS_Y_FIELD_NUMBER: _ClassVar[int]
    GYRO_BIAS_Z_FIELD_NUMBER: _ClassVar[int]
    gyro_bias_x: float
    gyro_bias_y: float
    gyro_bias_z: float
    def __init__(self, gyro_bias_x: _Optional[float] = ..., gyro_bias_y: _Optional[float] = ..., gyro_bias_z: _Optional[float] = ...) -> None: ...

class SetImuCalibrationResponse(_message.Message):
    __slots__ = ["success"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    success: bool
    def __init__(self, success: bool = ...) -> None: ...
