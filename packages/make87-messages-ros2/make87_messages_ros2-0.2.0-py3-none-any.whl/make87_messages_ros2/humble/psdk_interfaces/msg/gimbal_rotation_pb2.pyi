from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GimbalRotation(_message.Message):
    __slots__ = ["header", "payload_index", "rotation_mode", "pitch", "roll", "yaw", "time"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_INDEX_FIELD_NUMBER: _ClassVar[int]
    ROTATION_MODE_FIELD_NUMBER: _ClassVar[int]
    PITCH_FIELD_NUMBER: _ClassVar[int]
    ROLL_FIELD_NUMBER: _ClassVar[int]
    YAW_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    payload_index: int
    rotation_mode: int
    pitch: float
    roll: float
    yaw: float
    time: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., payload_index: _Optional[int] = ..., rotation_mode: _Optional[int] = ..., pitch: _Optional[float] = ..., roll: _Optional[float] = ..., yaw: _Optional[float] = ..., time: _Optional[float] = ...) -> None: ...
