from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class GpgsvSatellite(_message.Message):
    __slots__ = ["prn", "elevation", "azimuth", "snr"]
    PRN_FIELD_NUMBER: _ClassVar[int]
    ELEVATION_FIELD_NUMBER: _ClassVar[int]
    AZIMUTH_FIELD_NUMBER: _ClassVar[int]
    SNR_FIELD_NUMBER: _ClassVar[int]
    prn: int
    elevation: int
    azimuth: int
    snr: int
    def __init__(self, prn: _Optional[int] = ..., elevation: _Optional[int] = ..., azimuth: _Optional[int] = ..., snr: _Optional[int] = ...) -> None: ...
