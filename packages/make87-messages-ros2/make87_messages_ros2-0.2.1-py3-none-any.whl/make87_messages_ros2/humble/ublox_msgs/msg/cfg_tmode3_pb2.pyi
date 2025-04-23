from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CfgTMODE3(_message.Message):
    __slots__ = ["header", "version", "reserved1", "flags", "ecef_x_or_lat", "ecef_y_or_lon", "ecef_z_or_alt", "ecef_x_or_lat_hp", "ecef_y_or_lon_hp", "ecef_z_or_alt_hp", "reserved2", "fixed_pos_acc", "svin_min_dur", "svin_acc_limit", "reserved3"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    RESERVED1_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    ECEF_X_OR_LAT_FIELD_NUMBER: _ClassVar[int]
    ECEF_Y_OR_LON_FIELD_NUMBER: _ClassVar[int]
    ECEF_Z_OR_ALT_FIELD_NUMBER: _ClassVar[int]
    ECEF_X_OR_LAT_HP_FIELD_NUMBER: _ClassVar[int]
    ECEF_Y_OR_LON_HP_FIELD_NUMBER: _ClassVar[int]
    ECEF_Z_OR_ALT_HP_FIELD_NUMBER: _ClassVar[int]
    RESERVED2_FIELD_NUMBER: _ClassVar[int]
    FIXED_POS_ACC_FIELD_NUMBER: _ClassVar[int]
    SVIN_MIN_DUR_FIELD_NUMBER: _ClassVar[int]
    SVIN_ACC_LIMIT_FIELD_NUMBER: _ClassVar[int]
    RESERVED3_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    version: int
    reserved1: int
    flags: int
    ecef_x_or_lat: int
    ecef_y_or_lon: int
    ecef_z_or_alt: int
    ecef_x_or_lat_hp: int
    ecef_y_or_lon_hp: int
    ecef_z_or_alt_hp: int
    reserved2: int
    fixed_pos_acc: int
    svin_min_dur: int
    svin_acc_limit: int
    reserved3: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., version: _Optional[int] = ..., reserved1: _Optional[int] = ..., flags: _Optional[int] = ..., ecef_x_or_lat: _Optional[int] = ..., ecef_y_or_lon: _Optional[int] = ..., ecef_z_or_alt: _Optional[int] = ..., ecef_x_or_lat_hp: _Optional[int] = ..., ecef_y_or_lon_hp: _Optional[int] = ..., ecef_z_or_alt_hp: _Optional[int] = ..., reserved2: _Optional[int] = ..., fixed_pos_acc: _Optional[int] = ..., svin_min_dur: _Optional[int] = ..., svin_acc_limit: _Optional[int] = ..., reserved3: _Optional[_Iterable[int]] = ...) -> None: ...
