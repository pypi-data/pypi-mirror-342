from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CommandHomeRequest(_message.Message):
    __slots__ = ["header", "current_gps", "yaw", "latitude", "longitude", "altitude"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    CURRENT_GPS_FIELD_NUMBER: _ClassVar[int]
    YAW_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    current_gps: bool
    yaw: float
    latitude: float
    longitude: float
    altitude: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., current_gps: bool = ..., yaw: _Optional[float] = ..., latitude: _Optional[float] = ..., longitude: _Optional[float] = ..., altitude: _Optional[float] = ...) -> None: ...

class CommandHomeResponse(_message.Message):
    __slots__ = ["header", "success", "result"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    RESULT_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    result: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., result: _Optional[int] = ...) -> None: ...
