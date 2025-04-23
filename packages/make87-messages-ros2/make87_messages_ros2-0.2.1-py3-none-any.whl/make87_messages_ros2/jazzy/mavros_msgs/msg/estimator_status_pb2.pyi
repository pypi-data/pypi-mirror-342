from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class EstimatorStatus(_message.Message):
    __slots__ = ["header", "attitude_status_flag", "velocity_horiz_status_flag", "velocity_vert_status_flag", "pos_horiz_rel_status_flag", "pos_horiz_abs_status_flag", "pos_vert_abs_status_flag", "pos_vert_agl_status_flag", "const_pos_mode_status_flag", "pred_pos_horiz_rel_status_flag", "pred_pos_horiz_abs_status_flag", "gps_glitch_status_flag", "accel_error_status_flag"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ATTITUDE_STATUS_FLAG_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_HORIZ_STATUS_FLAG_FIELD_NUMBER: _ClassVar[int]
    VELOCITY_VERT_STATUS_FLAG_FIELD_NUMBER: _ClassVar[int]
    POS_HORIZ_REL_STATUS_FLAG_FIELD_NUMBER: _ClassVar[int]
    POS_HORIZ_ABS_STATUS_FLAG_FIELD_NUMBER: _ClassVar[int]
    POS_VERT_ABS_STATUS_FLAG_FIELD_NUMBER: _ClassVar[int]
    POS_VERT_AGL_STATUS_FLAG_FIELD_NUMBER: _ClassVar[int]
    CONST_POS_MODE_STATUS_FLAG_FIELD_NUMBER: _ClassVar[int]
    PRED_POS_HORIZ_REL_STATUS_FLAG_FIELD_NUMBER: _ClassVar[int]
    PRED_POS_HORIZ_ABS_STATUS_FLAG_FIELD_NUMBER: _ClassVar[int]
    GPS_GLITCH_STATUS_FLAG_FIELD_NUMBER: _ClassVar[int]
    ACCEL_ERROR_STATUS_FLAG_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    attitude_status_flag: bool
    velocity_horiz_status_flag: bool
    velocity_vert_status_flag: bool
    pos_horiz_rel_status_flag: bool
    pos_horiz_abs_status_flag: bool
    pos_vert_abs_status_flag: bool
    pos_vert_agl_status_flag: bool
    const_pos_mode_status_flag: bool
    pred_pos_horiz_rel_status_flag: bool
    pred_pos_horiz_abs_status_flag: bool
    gps_glitch_status_flag: bool
    accel_error_status_flag: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., attitude_status_flag: bool = ..., velocity_horiz_status_flag: bool = ..., velocity_vert_status_flag: bool = ..., pos_horiz_rel_status_flag: bool = ..., pos_horiz_abs_status_flag: bool = ..., pos_vert_abs_status_flag: bool = ..., pos_vert_agl_status_flag: bool = ..., const_pos_mode_status_flag: bool = ..., pred_pos_horiz_rel_status_flag: bool = ..., pred_pos_horiz_abs_status_flag: bool = ..., gps_glitch_status_flag: bool = ..., accel_error_status_flag: bool = ...) -> None: ...
