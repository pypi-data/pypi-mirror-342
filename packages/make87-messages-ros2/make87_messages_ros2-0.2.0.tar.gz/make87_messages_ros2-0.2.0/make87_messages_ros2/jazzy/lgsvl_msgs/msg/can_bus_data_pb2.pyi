from make87_messages_ros2.jazzy.geometry_msgs.msg import quaternion_pb2 as _quaternion_pb2
from make87_messages_ros2.jazzy.geometry_msgs.msg import vector3_pb2 as _vector3_pb2
from make87_messages_ros2.jazzy.std_msgs.msg import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CanBusData(_message.Message):
    __slots__ = ["header", "speed_mps", "throttle_pct", "brake_pct", "steer_pct", "parking_brake_active", "high_beams_active", "low_beams_active", "hazard_lights_active", "fog_lights_active", "left_turn_signal_active", "right_turn_signal_active", "wipers_active", "reverse_gear_active", "selected_gear", "engine_active", "engine_rpm", "gps_latitude", "gps_longitude", "gps_altitude", "orientation", "linear_velocities"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    SPEED_MPS_FIELD_NUMBER: _ClassVar[int]
    THROTTLE_PCT_FIELD_NUMBER: _ClassVar[int]
    BRAKE_PCT_FIELD_NUMBER: _ClassVar[int]
    STEER_PCT_FIELD_NUMBER: _ClassVar[int]
    PARKING_BRAKE_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    HIGH_BEAMS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    LOW_BEAMS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    HAZARD_LIGHTS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    FOG_LIGHTS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    LEFT_TURN_SIGNAL_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    RIGHT_TURN_SIGNAL_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    WIPERS_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    REVERSE_GEAR_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    SELECTED_GEAR_FIELD_NUMBER: _ClassVar[int]
    ENGINE_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    ENGINE_RPM_FIELD_NUMBER: _ClassVar[int]
    GPS_LATITUDE_FIELD_NUMBER: _ClassVar[int]
    GPS_LONGITUDE_FIELD_NUMBER: _ClassVar[int]
    GPS_ALTITUDE_FIELD_NUMBER: _ClassVar[int]
    ORIENTATION_FIELD_NUMBER: _ClassVar[int]
    LINEAR_VELOCITIES_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    speed_mps: float
    throttle_pct: float
    brake_pct: float
    steer_pct: float
    parking_brake_active: bool
    high_beams_active: bool
    low_beams_active: bool
    hazard_lights_active: bool
    fog_lights_active: bool
    left_turn_signal_active: bool
    right_turn_signal_active: bool
    wipers_active: bool
    reverse_gear_active: bool
    selected_gear: int
    engine_active: bool
    engine_rpm: float
    gps_latitude: float
    gps_longitude: float
    gps_altitude: float
    orientation: _quaternion_pb2.Quaternion
    linear_velocities: _vector3_pb2.Vector3
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., speed_mps: _Optional[float] = ..., throttle_pct: _Optional[float] = ..., brake_pct: _Optional[float] = ..., steer_pct: _Optional[float] = ..., parking_brake_active: bool = ..., high_beams_active: bool = ..., low_beams_active: bool = ..., hazard_lights_active: bool = ..., fog_lights_active: bool = ..., left_turn_signal_active: bool = ..., right_turn_signal_active: bool = ..., wipers_active: bool = ..., reverse_gear_active: bool = ..., selected_gear: _Optional[int] = ..., engine_active: bool = ..., engine_rpm: _Optional[float] = ..., gps_latitude: _Optional[float] = ..., gps_longitude: _Optional[float] = ..., gps_altitude: _Optional[float] = ..., orientation: _Optional[_Union[_quaternion_pb2.Quaternion, _Mapping]] = ..., linear_velocities: _Optional[_Union[_vector3_pb2.Vector3, _Mapping]] = ...) -> None: ...
