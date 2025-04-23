from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ResetPoseRequest(_message.Message):
    __slots__ = ["x", "y", "z", "roll", "pitch", "yaw"]
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    Z_FIELD_NUMBER: _ClassVar[int]
    ROLL_FIELD_NUMBER: _ClassVar[int]
    PITCH_FIELD_NUMBER: _ClassVar[int]
    YAW_FIELD_NUMBER: _ClassVar[int]
    x: float
    y: float
    z: float
    roll: float
    pitch: float
    yaw: float
    def __init__(self, x: _Optional[float] = ..., y: _Optional[float] = ..., z: _Optional[float] = ..., roll: _Optional[float] = ..., pitch: _Optional[float] = ..., yaw: _Optional[float] = ...) -> None: ...

class ResetPoseResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
