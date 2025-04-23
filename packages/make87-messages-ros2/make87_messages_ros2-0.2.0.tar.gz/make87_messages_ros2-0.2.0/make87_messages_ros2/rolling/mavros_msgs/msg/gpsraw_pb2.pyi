from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GPSRAW(_message.Message):
    __slots__ = ["header", "fix_type", "lat", "lon", "alt", "eph", "epv", "vel", "cog", "satellites_visible", "alt_ellipsoid", "h_acc", "v_acc", "vel_acc", "hdg_acc", "yaw", "dgps_numch", "dgps_age"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    FIX_TYPE_FIELD_NUMBER: _ClassVar[int]
    LAT_FIELD_NUMBER: _ClassVar[int]
    LON_FIELD_NUMBER: _ClassVar[int]
    ALT_FIELD_NUMBER: _ClassVar[int]
    EPH_FIELD_NUMBER: _ClassVar[int]
    EPV_FIELD_NUMBER: _ClassVar[int]
    VEL_FIELD_NUMBER: _ClassVar[int]
    COG_FIELD_NUMBER: _ClassVar[int]
    SATELLITES_VISIBLE_FIELD_NUMBER: _ClassVar[int]
    ALT_ELLIPSOID_FIELD_NUMBER: _ClassVar[int]
    H_ACC_FIELD_NUMBER: _ClassVar[int]
    V_ACC_FIELD_NUMBER: _ClassVar[int]
    VEL_ACC_FIELD_NUMBER: _ClassVar[int]
    HDG_ACC_FIELD_NUMBER: _ClassVar[int]
    YAW_FIELD_NUMBER: _ClassVar[int]
    DGPS_NUMCH_FIELD_NUMBER: _ClassVar[int]
    DGPS_AGE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    fix_type: int
    lat: int
    lon: int
    alt: int
    eph: int
    epv: int
    vel: int
    cog: int
    satellites_visible: int
    alt_ellipsoid: int
    h_acc: int
    v_acc: int
    vel_acc: int
    hdg_acc: int
    yaw: int
    dgps_numch: int
    dgps_age: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., fix_type: _Optional[int] = ..., lat: _Optional[int] = ..., lon: _Optional[int] = ..., alt: _Optional[int] = ..., eph: _Optional[int] = ..., epv: _Optional[int] = ..., vel: _Optional[int] = ..., cog: _Optional[int] = ..., satellites_visible: _Optional[int] = ..., alt_ellipsoid: _Optional[int] = ..., h_acc: _Optional[int] = ..., v_acc: _Optional[int] = ..., vel_acc: _Optional[int] = ..., hdg_acc: _Optional[int] = ..., yaw: _Optional[int] = ..., dgps_numch: _Optional[int] = ..., dgps_age: _Optional[int] = ...) -> None: ...
