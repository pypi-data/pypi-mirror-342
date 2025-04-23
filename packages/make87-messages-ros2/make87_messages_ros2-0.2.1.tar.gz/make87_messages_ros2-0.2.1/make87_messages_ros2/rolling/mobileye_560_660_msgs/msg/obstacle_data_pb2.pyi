from make87_messages_ros2.rolling.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ObstacleData(_message.Message):
    __slots__ = ["header", "obstacle_id", "obstacle_pos_x", "obstacle_pos_y", "blinker_info", "cut_in_and_out", "obstacle_rel_vel_x", "obstacle_type", "obstacle_status", "obstacle_brake_lights", "obstacle_valid", "obstacle_length", "obstacle_width", "obstacle_age", "obstacle_lane", "cipv_flag", "radar_pos_x", "radar_vel_x", "radar_match_confidence", "matched_radar_id", "obstacle_angle_rate", "obstacle_scale_change", "object_accel_x", "obstacle_replaced", "obstacle_angle"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    OBSTACLE_ID_FIELD_NUMBER: _ClassVar[int]
    OBSTACLE_POS_X_FIELD_NUMBER: _ClassVar[int]
    OBSTACLE_POS_Y_FIELD_NUMBER: _ClassVar[int]
    BLINKER_INFO_FIELD_NUMBER: _ClassVar[int]
    CUT_IN_AND_OUT_FIELD_NUMBER: _ClassVar[int]
    OBSTACLE_REL_VEL_X_FIELD_NUMBER: _ClassVar[int]
    OBSTACLE_TYPE_FIELD_NUMBER: _ClassVar[int]
    OBSTACLE_STATUS_FIELD_NUMBER: _ClassVar[int]
    OBSTACLE_BRAKE_LIGHTS_FIELD_NUMBER: _ClassVar[int]
    OBSTACLE_VALID_FIELD_NUMBER: _ClassVar[int]
    OBSTACLE_LENGTH_FIELD_NUMBER: _ClassVar[int]
    OBSTACLE_WIDTH_FIELD_NUMBER: _ClassVar[int]
    OBSTACLE_AGE_FIELD_NUMBER: _ClassVar[int]
    OBSTACLE_LANE_FIELD_NUMBER: _ClassVar[int]
    CIPV_FLAG_FIELD_NUMBER: _ClassVar[int]
    RADAR_POS_X_FIELD_NUMBER: _ClassVar[int]
    RADAR_VEL_X_FIELD_NUMBER: _ClassVar[int]
    RADAR_MATCH_CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    MATCHED_RADAR_ID_FIELD_NUMBER: _ClassVar[int]
    OBSTACLE_ANGLE_RATE_FIELD_NUMBER: _ClassVar[int]
    OBSTACLE_SCALE_CHANGE_FIELD_NUMBER: _ClassVar[int]
    OBJECT_ACCEL_X_FIELD_NUMBER: _ClassVar[int]
    OBSTACLE_REPLACED_FIELD_NUMBER: _ClassVar[int]
    OBSTACLE_ANGLE_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    obstacle_id: int
    obstacle_pos_x: float
    obstacle_pos_y: float
    blinker_info: int
    cut_in_and_out: int
    obstacle_rel_vel_x: float
    obstacle_type: int
    obstacle_status: int
    obstacle_brake_lights: bool
    obstacle_valid: int
    obstacle_length: float
    obstacle_width: float
    obstacle_age: int
    obstacle_lane: int
    cipv_flag: bool
    radar_pos_x: float
    radar_vel_x: float
    radar_match_confidence: int
    matched_radar_id: int
    obstacle_angle_rate: float
    obstacle_scale_change: float
    object_accel_x: float
    obstacle_replaced: bool
    obstacle_angle: float
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., obstacle_id: _Optional[int] = ..., obstacle_pos_x: _Optional[float] = ..., obstacle_pos_y: _Optional[float] = ..., blinker_info: _Optional[int] = ..., cut_in_and_out: _Optional[int] = ..., obstacle_rel_vel_x: _Optional[float] = ..., obstacle_type: _Optional[int] = ..., obstacle_status: _Optional[int] = ..., obstacle_brake_lights: bool = ..., obstacle_valid: _Optional[int] = ..., obstacle_length: _Optional[float] = ..., obstacle_width: _Optional[float] = ..., obstacle_age: _Optional[int] = ..., obstacle_lane: _Optional[int] = ..., cipv_flag: bool = ..., radar_pos_x: _Optional[float] = ..., radar_vel_x: _Optional[float] = ..., radar_match_confidence: _Optional[int] = ..., matched_radar_id: _Optional[int] = ..., obstacle_angle_rate: _Optional[float] = ..., obstacle_scale_change: _Optional[float] = ..., object_accel_x: _Optional[float] = ..., obstacle_replaced: bool = ..., obstacle_angle: _Optional[float] = ...) -> None: ...
