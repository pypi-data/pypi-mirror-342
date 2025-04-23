from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GimbalDeviceInformation(_message.Message):
    __slots__ = ["header", "vendor_name", "model_name", "custom_name", "firmware_version", "hardware_version", "uid", "cap_flags", "custom_cap_flags", "roll_min", "roll_max", "pitch_min", "pitch_max", "yaw_min", "yaw_max"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    VENDOR_NAME_FIELD_NUMBER: _ClassVar[int]
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_NAME_FIELD_NUMBER: _ClassVar[int]
    FIRMWARE_VERSION_FIELD_NUMBER: _ClassVar[int]
    HARDWARE_VERSION_FIELD_NUMBER: _ClassVar[int]
    UID_FIELD_NUMBER: _ClassVar[int]
    CAP_FLAGS_FIELD_NUMBER: _ClassVar[int]
    CUSTOM_CAP_FLAGS_FIELD_NUMBER: _ClassVar[int]
    ROLL_MIN_FIELD_NUMBER: _ClassVar[int]
    ROLL_MAX_FIELD_NUMBER: _ClassVar[int]
    PITCH_MIN_FIELD_NUMBER: _ClassVar[int]
    PITCH_MAX_FIELD_NUMBER: _ClassVar[int]
    YAW_MIN_FIELD_NUMBER: _ClassVar[int]
    YAW_MAX_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    vendor_name: str
    model_name: str
    custom_name: str
    firmware_version: int
    hardware_version: int
    uid: int
    cap_flags: int
    custom_cap_flags: int
    roll_min: float
    roll_max: float
    pitch_min: float
    pitch_max: float
    yaw_min: float
    yaw_max: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., vendor_name: _Optional[str] = ..., model_name: _Optional[str] = ..., custom_name: _Optional[str] = ..., firmware_version: _Optional[int] = ..., hardware_version: _Optional[int] = ..., uid: _Optional[int] = ..., cap_flags: _Optional[int] = ..., custom_cap_flags: _Optional[int] = ..., roll_min: _Optional[float] = ..., roll_max: _Optional[float] = ..., pitch_min: _Optional[float] = ..., pitch_max: _Optional[float] = ..., yaw_min: _Optional[float] = ..., yaw_max: _Optional[float] = ...) -> None: ...
