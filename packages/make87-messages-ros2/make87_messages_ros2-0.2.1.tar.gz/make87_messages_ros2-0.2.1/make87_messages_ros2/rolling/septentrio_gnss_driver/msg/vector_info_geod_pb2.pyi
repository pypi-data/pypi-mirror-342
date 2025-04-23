from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class VectorInfoGeod(_message.Message):
    __slots__ = ["nr_sv", "error", "mode", "misc", "delta_east", "delta_north", "delta_up", "delta_ve", "delta_vn", "delta_vu", "azimuth", "elevation", "reference_id", "corr_age", "signal_info"]
    NR_SV_FIELD_NUMBER: _ClassVar[int]
    ERROR_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    MISC_FIELD_NUMBER: _ClassVar[int]
    DELTA_EAST_FIELD_NUMBER: _ClassVar[int]
    DELTA_NORTH_FIELD_NUMBER: _ClassVar[int]
    DELTA_UP_FIELD_NUMBER: _ClassVar[int]
    DELTA_VE_FIELD_NUMBER: _ClassVar[int]
    DELTA_VN_FIELD_NUMBER: _ClassVar[int]
    DELTA_VU_FIELD_NUMBER: _ClassVar[int]
    AZIMUTH_FIELD_NUMBER: _ClassVar[int]
    ELEVATION_FIELD_NUMBER: _ClassVar[int]
    REFERENCE_ID_FIELD_NUMBER: _ClassVar[int]
    CORR_AGE_FIELD_NUMBER: _ClassVar[int]
    SIGNAL_INFO_FIELD_NUMBER: _ClassVar[int]
    nr_sv: int
    error: int
    mode: int
    misc: int
    delta_east: float
    delta_north: float
    delta_up: float
    delta_ve: float
    delta_vn: float
    delta_vu: float
    azimuth: int
    elevation: int
    reference_id: int
    corr_age: int
    signal_info: int
    def __init__(self, nr_sv: _Optional[int] = ..., error: _Optional[int] = ..., mode: _Optional[int] = ..., misc: _Optional[int] = ..., delta_east: _Optional[float] = ..., delta_north: _Optional[float] = ..., delta_up: _Optional[float] = ..., delta_ve: _Optional[float] = ..., delta_vn: _Optional[float] = ..., delta_vu: _Optional[float] = ..., azimuth: _Optional[int] = ..., elevation: _Optional[int] = ..., reference_id: _Optional[int] = ..., corr_age: _Optional[int] = ..., signal_info: _Optional[int] = ...) -> None: ...
