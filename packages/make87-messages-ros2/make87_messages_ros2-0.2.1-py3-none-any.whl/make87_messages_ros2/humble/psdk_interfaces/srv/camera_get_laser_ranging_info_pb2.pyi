from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CameraGetLaserRangingInfoRequest(_message.Message):
    __slots__ = ["header", "payload_index"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_INDEX_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    payload_index: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., payload_index: _Optional[int] = ...) -> None: ...

class CameraGetLaserRangingInfoResponse(_message.Message):
    __slots__ = ["header", "success", "longitude", "latitude", "altitude", "distance", "screen_x", "screen_y", "enable_lidar", "exception"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_FIELD_NUMBER: _ClassVar[int]
    DISTANCE_FIELD_NUMBER: _ClassVar[int]
    SCREEN_X_FIELD_NUMBER: _ClassVar[int]
    SCREEN_Y_FIELD_NUMBER: _ClassVar[int]
    ENABLE_LIDAR_FIELD_NUMBER: _ClassVar[int]
    EXCEPTION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    success: bool
    longitude: float
    latitude: float
    altitude: int
    distance: int
    screen_x: int
    screen_y: int
    enable_lidar: bool
    exception: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., success: bool = ..., longitude: _Optional[float] = ..., latitude: _Optional[float] = ..., altitude: _Optional[int] = ..., distance: _Optional[int] = ..., screen_x: _Optional[int] = ..., screen_y: _Optional[int] = ..., enable_lidar: bool = ..., exception: _Optional[int] = ...) -> None: ...
