from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.ibeo_msgs.msg import ibeo_data_header_pb2 as _ibeo_data_header_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ErrorWarning(_message.Message):
    __slots__ = ["header", "ros2_header", "ibeo_header", "err_internal_error", "err_motor_1_fault", "err_buffer_error_xmt_incomplete", "err_buffer_error_overflow", "err_apd_over_temperature", "err_apd_under_temperature", "err_apd_temperature_sensor_defect", "err_motor_2_fault", "err_motor_3_fault", "err_motor_4_fault", "err_motor_5_fault", "err_int_no_scan_data", "err_int_communication_error", "err_int_incorrect_scan_data", "err_config_fpga_not_configurable", "err_config_incorrect_config_data", "err_config_contains_incorrect_params", "err_timeout_data_processing", "err_timeout_env_model_computation_reset", "wrn_int_communication_error", "wrn_low_temperature", "wrn_high_temperature", "wrn_int_motor_1", "wrn_sync_error", "wrn_laser_1_start_pulse_missing", "wrn_laser_2_start_pulse_missing", "wrn_can_interface_blocked", "wrn_eth_interface_blocked", "wrn_incorrect_can_data_rcvd", "wrn_int_incorrect_scan_data", "wrn_eth_unkwn_incomplete_data", "wrn_incorrect_or_forbidden_cmd_rcvd", "wrn_memory_access_failure", "wrn_int_overflow", "wrn_ego_motion_data_missing", "wrn_incorrect_mounting_params", "wrn_no_obj_comp_due_to_scan_freq"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    IBEO_HEADER_FIELD_NUMBER: _ClassVar[int]
    ERR_INTERNAL_ERROR_FIELD_NUMBER: _ClassVar[int]
    ERR_MOTOR_1_FAULT_FIELD_NUMBER: _ClassVar[int]
    ERR_BUFFER_ERROR_XMT_INCOMPLETE_FIELD_NUMBER: _ClassVar[int]
    ERR_BUFFER_ERROR_OVERFLOW_FIELD_NUMBER: _ClassVar[int]
    ERR_APD_OVER_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    ERR_APD_UNDER_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    ERR_APD_TEMPERATURE_SENSOR_DEFECT_FIELD_NUMBER: _ClassVar[int]
    ERR_MOTOR_2_FAULT_FIELD_NUMBER: _ClassVar[int]
    ERR_MOTOR_3_FAULT_FIELD_NUMBER: _ClassVar[int]
    ERR_MOTOR_4_FAULT_FIELD_NUMBER: _ClassVar[int]
    ERR_MOTOR_5_FAULT_FIELD_NUMBER: _ClassVar[int]
    ERR_INT_NO_SCAN_DATA_FIELD_NUMBER: _ClassVar[int]
    ERR_INT_COMMUNICATION_ERROR_FIELD_NUMBER: _ClassVar[int]
    ERR_INT_INCORRECT_SCAN_DATA_FIELD_NUMBER: _ClassVar[int]
    ERR_CONFIG_FPGA_NOT_CONFIGURABLE_FIELD_NUMBER: _ClassVar[int]
    ERR_CONFIG_INCORRECT_CONFIG_DATA_FIELD_NUMBER: _ClassVar[int]
    ERR_CONFIG_CONTAINS_INCORRECT_PARAMS_FIELD_NUMBER: _ClassVar[int]
    ERR_TIMEOUT_DATA_PROCESSING_FIELD_NUMBER: _ClassVar[int]
    ERR_TIMEOUT_ENV_MODEL_COMPUTATION_RESET_FIELD_NUMBER: _ClassVar[int]
    WRN_INT_COMMUNICATION_ERROR_FIELD_NUMBER: _ClassVar[int]
    WRN_LOW_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    WRN_HIGH_TEMPERATURE_FIELD_NUMBER: _ClassVar[int]
    WRN_INT_MOTOR_1_FIELD_NUMBER: _ClassVar[int]
    WRN_SYNC_ERROR_FIELD_NUMBER: _ClassVar[int]
    WRN_LASER_1_START_PULSE_MISSING_FIELD_NUMBER: _ClassVar[int]
    WRN_LASER_2_START_PULSE_MISSING_FIELD_NUMBER: _ClassVar[int]
    WRN_CAN_INTERFACE_BLOCKED_FIELD_NUMBER: _ClassVar[int]
    WRN_ETH_INTERFACE_BLOCKED_FIELD_NUMBER: _ClassVar[int]
    WRN_INCORRECT_CAN_DATA_RCVD_FIELD_NUMBER: _ClassVar[int]
    WRN_INT_INCORRECT_SCAN_DATA_FIELD_NUMBER: _ClassVar[int]
    WRN_ETH_UNKWN_INCOMPLETE_DATA_FIELD_NUMBER: _ClassVar[int]
    WRN_INCORRECT_OR_FORBIDDEN_CMD_RCVD_FIELD_NUMBER: _ClassVar[int]
    WRN_MEMORY_ACCESS_FAILURE_FIELD_NUMBER: _ClassVar[int]
    WRN_INT_OVERFLOW_FIELD_NUMBER: _ClassVar[int]
    WRN_EGO_MOTION_DATA_MISSING_FIELD_NUMBER: _ClassVar[int]
    WRN_INCORRECT_MOUNTING_PARAMS_FIELD_NUMBER: _ClassVar[int]
    WRN_NO_OBJ_COMP_DUE_TO_SCAN_FREQ_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    ibeo_header: _ibeo_data_header_pb2.IbeoDataHeader
    err_internal_error: bool
    err_motor_1_fault: bool
    err_buffer_error_xmt_incomplete: bool
    err_buffer_error_overflow: bool
    err_apd_over_temperature: bool
    err_apd_under_temperature: bool
    err_apd_temperature_sensor_defect: bool
    err_motor_2_fault: bool
    err_motor_3_fault: bool
    err_motor_4_fault: bool
    err_motor_5_fault: bool
    err_int_no_scan_data: bool
    err_int_communication_error: bool
    err_int_incorrect_scan_data: bool
    err_config_fpga_not_configurable: bool
    err_config_incorrect_config_data: bool
    err_config_contains_incorrect_params: bool
    err_timeout_data_processing: bool
    err_timeout_env_model_computation_reset: bool
    wrn_int_communication_error: bool
    wrn_low_temperature: bool
    wrn_high_temperature: bool
    wrn_int_motor_1: bool
    wrn_sync_error: bool
    wrn_laser_1_start_pulse_missing: bool
    wrn_laser_2_start_pulse_missing: bool
    wrn_can_interface_blocked: bool
    wrn_eth_interface_blocked: bool
    wrn_incorrect_can_data_rcvd: bool
    wrn_int_incorrect_scan_data: bool
    wrn_eth_unkwn_incomplete_data: bool
    wrn_incorrect_or_forbidden_cmd_rcvd: bool
    wrn_memory_access_failure: bool
    wrn_int_overflow: bool
    wrn_ego_motion_data_missing: bool
    wrn_incorrect_mounting_params: bool
    wrn_no_obj_comp_due_to_scan_freq: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., ibeo_header: _Optional[_Union[_ibeo_data_header_pb2.IbeoDataHeader, _Mapping]] = ..., err_internal_error: bool = ..., err_motor_1_fault: bool = ..., err_buffer_error_xmt_incomplete: bool = ..., err_buffer_error_overflow: bool = ..., err_apd_over_temperature: bool = ..., err_apd_under_temperature: bool = ..., err_apd_temperature_sensor_defect: bool = ..., err_motor_2_fault: bool = ..., err_motor_3_fault: bool = ..., err_motor_4_fault: bool = ..., err_motor_5_fault: bool = ..., err_int_no_scan_data: bool = ..., err_int_communication_error: bool = ..., err_int_incorrect_scan_data: bool = ..., err_config_fpga_not_configurable: bool = ..., err_config_incorrect_config_data: bool = ..., err_config_contains_incorrect_params: bool = ..., err_timeout_data_processing: bool = ..., err_timeout_env_model_computation_reset: bool = ..., wrn_int_communication_error: bool = ..., wrn_low_temperature: bool = ..., wrn_high_temperature: bool = ..., wrn_int_motor_1: bool = ..., wrn_sync_error: bool = ..., wrn_laser_1_start_pulse_missing: bool = ..., wrn_laser_2_start_pulse_missing: bool = ..., wrn_can_interface_blocked: bool = ..., wrn_eth_interface_blocked: bool = ..., wrn_incorrect_can_data_rcvd: bool = ..., wrn_int_incorrect_scan_data: bool = ..., wrn_eth_unkwn_incomplete_data: bool = ..., wrn_incorrect_or_forbidden_cmd_rcvd: bool = ..., wrn_memory_access_failure: bool = ..., wrn_int_overflow: bool = ..., wrn_ego_motion_data_missing: bool = ..., wrn_incorrect_mounting_params: bool = ..., wrn_no_obj_comp_due_to_scan_freq: bool = ...) -> None: ...
