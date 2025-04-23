from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ThrottleDiagnostics(_message.Message):
    __slots__ = ["header", "ros2_header", "degraded", "degraded_cmd_type", "degraded_comms", "degraded_comms_dbw", "degraded_comms_dbw_gateway", "degraded_comms_dbw_steer", "degraded_comms_dbw_brake", "degraded_comms_dbw_gear", "degraded_internal", "degraded_control_performance", "degraded_param_mismatch", "degraded_vehicle", "degraded_vehicle_speed", "degraded_aped_feedback", "degraded_actuator_pedal_sensor", "degraded_sensor", "degraded_calibration", "fault", "fault_power", "fault_comms", "fault_comms_dbw", "fault_comms_dbw_gateway", "fault_comms_dbw_steer", "fault_comms_dbw_brake", "fault_comms_dbw_gear", "fault_internal", "fault_vehicle", "fault_vehicle_speed", "fault_sensor", "fault_aped_sensor_1", "fault_aped_sensor_2", "fault_aped_sensor_mismatch", "fault_actuator_pedal_sensor", "fault_control_performance", "fault_param_mismatch", "fault_param_limits", "fault_calibration"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    DEGRADED_FIELD_NUMBER: _ClassVar[int]
    DEGRADED_CMD_TYPE_FIELD_NUMBER: _ClassVar[int]
    DEGRADED_COMMS_FIELD_NUMBER: _ClassVar[int]
    DEGRADED_COMMS_DBW_FIELD_NUMBER: _ClassVar[int]
    DEGRADED_COMMS_DBW_GATEWAY_FIELD_NUMBER: _ClassVar[int]
    DEGRADED_COMMS_DBW_STEER_FIELD_NUMBER: _ClassVar[int]
    DEGRADED_COMMS_DBW_BRAKE_FIELD_NUMBER: _ClassVar[int]
    DEGRADED_COMMS_DBW_GEAR_FIELD_NUMBER: _ClassVar[int]
    DEGRADED_INTERNAL_FIELD_NUMBER: _ClassVar[int]
    DEGRADED_CONTROL_PERFORMANCE_FIELD_NUMBER: _ClassVar[int]
    DEGRADED_PARAM_MISMATCH_FIELD_NUMBER: _ClassVar[int]
    DEGRADED_VEHICLE_FIELD_NUMBER: _ClassVar[int]
    DEGRADED_VEHICLE_SPEED_FIELD_NUMBER: _ClassVar[int]
    DEGRADED_APED_FEEDBACK_FIELD_NUMBER: _ClassVar[int]
    DEGRADED_ACTUATOR_PEDAL_SENSOR_FIELD_NUMBER: _ClassVar[int]
    DEGRADED_SENSOR_FIELD_NUMBER: _ClassVar[int]
    DEGRADED_CALIBRATION_FIELD_NUMBER: _ClassVar[int]
    FAULT_FIELD_NUMBER: _ClassVar[int]
    FAULT_POWER_FIELD_NUMBER: _ClassVar[int]
    FAULT_COMMS_FIELD_NUMBER: _ClassVar[int]
    FAULT_COMMS_DBW_FIELD_NUMBER: _ClassVar[int]
    FAULT_COMMS_DBW_GATEWAY_FIELD_NUMBER: _ClassVar[int]
    FAULT_COMMS_DBW_STEER_FIELD_NUMBER: _ClassVar[int]
    FAULT_COMMS_DBW_BRAKE_FIELD_NUMBER: _ClassVar[int]
    FAULT_COMMS_DBW_GEAR_FIELD_NUMBER: _ClassVar[int]
    FAULT_INTERNAL_FIELD_NUMBER: _ClassVar[int]
    FAULT_VEHICLE_FIELD_NUMBER: _ClassVar[int]
    FAULT_VEHICLE_SPEED_FIELD_NUMBER: _ClassVar[int]
    FAULT_SENSOR_FIELD_NUMBER: _ClassVar[int]
    FAULT_APED_SENSOR_1_FIELD_NUMBER: _ClassVar[int]
    FAULT_APED_SENSOR_2_FIELD_NUMBER: _ClassVar[int]
    FAULT_APED_SENSOR_MISMATCH_FIELD_NUMBER: _ClassVar[int]
    FAULT_ACTUATOR_PEDAL_SENSOR_FIELD_NUMBER: _ClassVar[int]
    FAULT_CONTROL_PERFORMANCE_FIELD_NUMBER: _ClassVar[int]
    FAULT_PARAM_MISMATCH_FIELD_NUMBER: _ClassVar[int]
    FAULT_PARAM_LIMITS_FIELD_NUMBER: _ClassVar[int]
    FAULT_CALIBRATION_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    degraded: bool
    degraded_cmd_type: bool
    degraded_comms: bool
    degraded_comms_dbw: bool
    degraded_comms_dbw_gateway: bool
    degraded_comms_dbw_steer: bool
    degraded_comms_dbw_brake: bool
    degraded_comms_dbw_gear: bool
    degraded_internal: bool
    degraded_control_performance: bool
    degraded_param_mismatch: bool
    degraded_vehicle: bool
    degraded_vehicle_speed: bool
    degraded_aped_feedback: bool
    degraded_actuator_pedal_sensor: bool
    degraded_sensor: bool
    degraded_calibration: bool
    fault: bool
    fault_power: bool
    fault_comms: bool
    fault_comms_dbw: bool
    fault_comms_dbw_gateway: bool
    fault_comms_dbw_steer: bool
    fault_comms_dbw_brake: bool
    fault_comms_dbw_gear: bool
    fault_internal: bool
    fault_vehicle: bool
    fault_vehicle_speed: bool
    fault_sensor: bool
    fault_aped_sensor_1: bool
    fault_aped_sensor_2: bool
    fault_aped_sensor_mismatch: bool
    fault_actuator_pedal_sensor: bool
    fault_control_performance: bool
    fault_param_mismatch: bool
    fault_param_limits: bool
    fault_calibration: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., degraded: bool = ..., degraded_cmd_type: bool = ..., degraded_comms: bool = ..., degraded_comms_dbw: bool = ..., degraded_comms_dbw_gateway: bool = ..., degraded_comms_dbw_steer: bool = ..., degraded_comms_dbw_brake: bool = ..., degraded_comms_dbw_gear: bool = ..., degraded_internal: bool = ..., degraded_control_performance: bool = ..., degraded_param_mismatch: bool = ..., degraded_vehicle: bool = ..., degraded_vehicle_speed: bool = ..., degraded_aped_feedback: bool = ..., degraded_actuator_pedal_sensor: bool = ..., degraded_sensor: bool = ..., degraded_calibration: bool = ..., fault: bool = ..., fault_power: bool = ..., fault_comms: bool = ..., fault_comms_dbw: bool = ..., fault_comms_dbw_gateway: bool = ..., fault_comms_dbw_steer: bool = ..., fault_comms_dbw_brake: bool = ..., fault_comms_dbw_gear: bool = ..., fault_internal: bool = ..., fault_vehicle: bool = ..., fault_vehicle_speed: bool = ..., fault_sensor: bool = ..., fault_aped_sensor_1: bool = ..., fault_aped_sensor_2: bool = ..., fault_aped_sensor_mismatch: bool = ..., fault_actuator_pedal_sensor: bool = ..., fault_control_performance: bool = ..., fault_param_mismatch: bool = ..., fault_param_limits: bool = ..., fault_calibration: bool = ...) -> None: ...
