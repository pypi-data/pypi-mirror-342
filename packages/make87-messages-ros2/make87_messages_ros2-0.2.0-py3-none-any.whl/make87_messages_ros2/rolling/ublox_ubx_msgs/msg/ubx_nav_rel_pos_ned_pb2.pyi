from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from make87_messages_ros2.rolling.ublox_ubx_msgs.msg import carr_soln_pb2 as _carr_soln_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class UBXNavRelPosNED(_message.Message):
    __slots__ = ["header", "version", "ref_station_id", "itow", "rel_pos_n", "rel_pos_e", "rel_pos_d", "rel_pos_length", "rel_pos_heading", "rel_pos_hp_n", "rel_pos_hp_e", "rel_pos_hp_d", "rel_pos_hp_length", "acc_n", "acc_e", "acc_d", "acc_length", "acc_heading", "gnss_fix_ok", "diff_soln", "rel_pos_valid", "carr_soln", "is_moving", "ref_pos_miss", "ref_obs_miss", "rel_pos_heading_valid", "rel_pos_normalized"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    VERSION_FIELD_NUMBER: _ClassVar[int]
    REF_STATION_ID_FIELD_NUMBER: _ClassVar[int]
    ITOW_FIELD_NUMBER: _ClassVar[int]
    REL_POS_N_FIELD_NUMBER: _ClassVar[int]
    REL_POS_E_FIELD_NUMBER: _ClassVar[int]
    REL_POS_D_FIELD_NUMBER: _ClassVar[int]
    REL_POS_LENGTH_FIELD_NUMBER: _ClassVar[int]
    REL_POS_HEADING_FIELD_NUMBER: _ClassVar[int]
    REL_POS_HP_N_FIELD_NUMBER: _ClassVar[int]
    REL_POS_HP_E_FIELD_NUMBER: _ClassVar[int]
    REL_POS_HP_D_FIELD_NUMBER: _ClassVar[int]
    REL_POS_HP_LENGTH_FIELD_NUMBER: _ClassVar[int]
    ACC_N_FIELD_NUMBER: _ClassVar[int]
    ACC_E_FIELD_NUMBER: _ClassVar[int]
    ACC_D_FIELD_NUMBER: _ClassVar[int]
    ACC_LENGTH_FIELD_NUMBER: _ClassVar[int]
    ACC_HEADING_FIELD_NUMBER: _ClassVar[int]
    GNSS_FIX_OK_FIELD_NUMBER: _ClassVar[int]
    DIFF_SOLN_FIELD_NUMBER: _ClassVar[int]
    REL_POS_VALID_FIELD_NUMBER: _ClassVar[int]
    CARR_SOLN_FIELD_NUMBER: _ClassVar[int]
    IS_MOVING_FIELD_NUMBER: _ClassVar[int]
    REF_POS_MISS_FIELD_NUMBER: _ClassVar[int]
    REF_OBS_MISS_FIELD_NUMBER: _ClassVar[int]
    REL_POS_HEADING_VALID_FIELD_NUMBER: _ClassVar[int]
    REL_POS_NORMALIZED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    version: int
    ref_station_id: int
    itow: int
    rel_pos_n: int
    rel_pos_e: int
    rel_pos_d: int
    rel_pos_length: int
    rel_pos_heading: int
    rel_pos_hp_n: int
    rel_pos_hp_e: int
    rel_pos_hp_d: int
    rel_pos_hp_length: int
    acc_n: int
    acc_e: int
    acc_d: int
    acc_length: int
    acc_heading: int
    gnss_fix_ok: bool
    diff_soln: bool
    rel_pos_valid: bool
    carr_soln: _carr_soln_pb2.CarrSoln
    is_moving: bool
    ref_pos_miss: bool
    ref_obs_miss: bool
    rel_pos_heading_valid: bool
    rel_pos_normalized: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., version: _Optional[int] = ..., ref_station_id: _Optional[int] = ..., itow: _Optional[int] = ..., rel_pos_n: _Optional[int] = ..., rel_pos_e: _Optional[int] = ..., rel_pos_d: _Optional[int] = ..., rel_pos_length: _Optional[int] = ..., rel_pos_heading: _Optional[int] = ..., rel_pos_hp_n: _Optional[int] = ..., rel_pos_hp_e: _Optional[int] = ..., rel_pos_hp_d: _Optional[int] = ..., rel_pos_hp_length: _Optional[int] = ..., acc_n: _Optional[int] = ..., acc_e: _Optional[int] = ..., acc_d: _Optional[int] = ..., acc_length: _Optional[int] = ..., acc_heading: _Optional[int] = ..., gnss_fix_ok: bool = ..., diff_soln: bool = ..., rel_pos_valid: bool = ..., carr_soln: _Optional[_Union[_carr_soln_pb2.CarrSoln, _Mapping]] = ..., is_moving: bool = ..., ref_pos_miss: bool = ..., ref_obs_miss: bool = ..., rel_pos_heading_valid: bool = ..., rel_pos_normalized: bool = ...) -> None: ...
