from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GPS(_message.Message):
    __slots__ = ["stamp", "longitude", "latitude", "altitude", "error", "bearing"]
    STAMP_FIELD_NUMBER: _ClassVar[int]
    LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    LATITUDE_FIELD_NUMBER: _ClassVar[int]
    ALTITUDE_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    BEARING_FIELD_NUMBER: _ClassVar[int]
    stamp: float
    longitude: float
    latitude: float
    altitude: float
    error: float
    bearing: float
    def __init__(self, stamp: _Optional[float] = ..., longitude: _Optional[float] = ..., latitude: _Optional[float] = ..., altitude: _Optional[float] = ..., error: _Optional[float] = ..., bearing: _Optional[float] = ...) -> None: ...
