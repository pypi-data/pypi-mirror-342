from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GimbalManagerSetPitchyaw(_message.Message):
    __slots__ = ["header", "target_system", "target_component", "flags", "gimbal_device_id", "pitch", "yaw", "pitch_rate", "yaw_rate"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    TARGET_SYSTEM_FIELD_NUMBER: _ClassVar[int]
    TARGET_COMPONENT_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    GIMBAL_DEVICE_ID_FIELD_NUMBER: _ClassVar[int]
    PITCH_FIELD_NUMBER: _ClassVar[int]
    YAW_FIELD_NUMBER: _ClassVar[int]
    PITCH_RATE_FIELD_NUMBER: _ClassVar[int]
    YAW_RATE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    target_system: int
    target_component: int
    flags: int
    gimbal_device_id: int
    pitch: float
    yaw: float
    pitch_rate: float
    yaw_rate: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., target_system: _Optional[int] = ..., target_component: _Optional[int] = ..., flags: _Optional[int] = ..., gimbal_device_id: _Optional[int] = ..., pitch: _Optional[float] = ..., yaw: _Optional[float] = ..., pitch_rate: _Optional[float] = ..., yaw_rate: _Optional[float] = ...) -> None: ...
