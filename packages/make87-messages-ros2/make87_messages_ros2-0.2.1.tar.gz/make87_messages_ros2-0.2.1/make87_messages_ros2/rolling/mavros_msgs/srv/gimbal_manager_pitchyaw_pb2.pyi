from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GimbalManagerPitchyawRequest(_message.Message):
    __slots__ = ["pitch", "yaw", "pitch_rate", "yaw_rate", "flags", "gimbal_device_id"]
    PITCH_FIELD_NUMBER: _ClassVar[int]
    YAW_FIELD_NUMBER: _ClassVar[int]
    PITCH_RATE_FIELD_NUMBER: _ClassVar[int]
    YAW_RATE_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    GIMBAL_DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    pitch: float
    yaw: float
    pitch_rate: float
    yaw_rate: float
    flags: int
    gimbal_device_id: int
    def __init__(self, pitch: _Optional[float] = ..., yaw: _Optional[float] = ..., pitch_rate: _Optional[float] = ..., yaw_rate: _Optional[float] = ..., flags: _Optional[int] = ..., gimbal_device_id: _Optional[int] = ...) -> None: ...

class GimbalManagerPitchyawResponse(_message.Message):
    __slots__ = ["success", "result"]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    success: bool
    result: int
    def __init__(self, success: bool = ..., result: _Optional[int] = ...) -> None: ...
