from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SbgEkfStatus(_message.Message):
    __slots__ = ["header", "solution_mode", "attitude_valid", "heading_valid", "velocity_valid", "position_valid", "vert_ref_used", "mag_ref_used", "gps1_vel_used", "gps1_pos_used", "gps1_hdt_used", "gps2_vel_used", "gps2_pos_used", "gps2_hdt_used", "odo_used", "dvl_bt_used", "dvl_wt_used", "user_pos_used", "user_vel_used", "user_heading_used", "usbl_used", "air_data_used", "zupt_used", "align_valid", "depth_used"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SOLUTION_MODE_FIELD_NUMBER: _ClassVar[int]
    ATTITUDE_VALID_FIELD_NUMBER: _ClassVar[int]
    HEADING_VALID_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_VALID_FIELD_NUMBER: _ClassVar[int]
    POSITION_VALID_FIELD_NUMBER: _ClassVar[int]
    VERT_REF_USED_FIELD_NUMBER: _ClassVar[int]
    MAG_REF_USED_FIELD_NUMBER: _ClassVar[int]
    GPS1_VEL_USED_FIELD_NUMBER: _ClassVar[int]
    GPS1_POS_USED_FIELD_NUMBER: _ClassVar[int]
    GPS1_HDT_USED_FIELD_NUMBER: _ClassVar[int]
    GPS2_VEL_USED_FIELD_NUMBER: _ClassVar[int]
    GPS2_POS_USED_FIELD_NUMBER: _ClassVar[int]
    GPS2_HDT_USED_FIELD_NUMBER: _ClassVar[int]
    ODO_USED_FIELD_NUMBER: _ClassVar[int]
    DVL_BT_USED_FIELD_NUMBER: _ClassVar[int]
    DVL_WT_USED_FIELD_NUMBER: _ClassVar[int]
    USER_POS_USED_FIELD_NUMBER: _ClassVar[int]
    USER_VEL_USED_FIELD_NUMBER: _ClassVar[int]
    USER_HEADING_USED_FIELD_NUMBER: _ClassVar[int]
    USBL_USED_FIELD_NUMBER: _ClassVar[int]
    AIR_DATA_USED_FIELD_NUMBER: _ClassVar[int]
    ZUPT_USED_FIELD_NUMBER: _ClassVar[int]
    ALIGN_VALID_FIELD_NUMBER: _ClassVar[int]
    DEPTH_USED_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    solution_mode: int
    attitude_valid: bool
    heading_valid: bool
    velocity_valid: bool
    position_valid: bool
    vert_ref_used: bool
    mag_ref_used: bool
    gps1_vel_used: bool
    gps1_pos_used: bool
    gps1_hdt_used: bool
    gps2_vel_used: bool
    gps2_pos_used: bool
    gps2_hdt_used: bool
    odo_used: bool
    dvl_bt_used: bool
    dvl_wt_used: bool
    user_pos_used: bool
    user_vel_used: bool
    user_heading_used: bool
    usbl_used: bool
    air_data_used: bool
    zupt_used: bool
    align_valid: bool
    depth_used: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., solution_mode: _Optional[int] = ..., attitude_valid: bool = ..., heading_valid: bool = ..., velocity_valid: bool = ..., position_valid: bool = ..., vert_ref_used: bool = ..., mag_ref_used: bool = ..., gps1_vel_used: bool = ..., gps1_pos_used: bool = ..., gps1_hdt_used: bool = ..., gps2_vel_used: bool = ..., gps2_pos_used: bool = ..., gps2_hdt_used: bool = ..., odo_used: bool = ..., dvl_bt_used: bool = ..., dvl_wt_used: bool = ..., user_pos_used: bool = ..., user_vel_used: bool = ..., user_heading_used: bool = ..., usbl_used: bool = ..., air_data_used: bool = ..., zupt_used: bool = ..., align_valid: bool = ..., depth_used: bool = ...) -> None: ...
