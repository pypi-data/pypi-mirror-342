from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.ds_dbw_msgs.msg import cmd_src_pb2 as _cmd_src_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SteeringReport(_message.Message):
    __slots__ = ["header", "ros2_header", "steering_wheel_angle", "steering_column_torque", "cmd", "cmd_type", "limiting_value", "limiting_rate", "external_control", "ready", "enabled", "override_active", "override_other", "override_latched", "timeout", "fault", "bad_crc", "bad_rc", "degraded", "limit_rate", "limit_value", "cmd_src"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    STEERING_WHEEL_ANGLE_FIELD_NUMBER: _ClassVar[int]
    STEERING_COLUMN_TORQUE_FIELD_NUMBER: _ClassVar[int]
    CMD_FIELD_NUMBER: _ClassVar[int]
    CMD_TYPE_FIELD_NUMBER: _ClassVar[int]
    LIMITING_VALUE_FIELD_NUMBER: _ClassVar[int]
    LIMITING_RATE_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_CONTROL_FIELD_NUMBER: _ClassVar[int]
    READY_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_OTHER_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_LATCHED_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    FAULT_FIELD_NUMBER: _ClassVar[int]
    BAD_CRC_FIELD_NUMBER: _ClassVar[int]
    BAD_RC_FIELD_NUMBER: _ClassVar[int]
    DEGRADED_FIELD_NUMBER: _ClassVar[int]
    LIMIT_RATE_FIELD_NUMBER: _ClassVar[int]
    LIMIT_VALUE_FIELD_NUMBER: _ClassVar[int]
    CMD_SRC_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    steering_wheel_angle: float
    steering_column_torque: float
    cmd: float
    cmd_type: int
    limiting_value: bool
    limiting_rate: bool
    external_control: bool
    ready: bool
    enabled: bool
    override_active: bool
    override_other: bool
    override_latched: bool
    timeout: bool
    fault: bool
    bad_crc: bool
    bad_rc: bool
    degraded: bool
    limit_rate: float
    limit_value: float
    cmd_src: _cmd_src_pb2.CmdSrc
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., steering_wheel_angle: _Optional[float] = ..., steering_column_torque: _Optional[float] = ..., cmd: _Optional[float] = ..., cmd_type: _Optional[int] = ..., limiting_value: bool = ..., limiting_rate: bool = ..., external_control: bool = ..., ready: bool = ..., enabled: bool = ..., override_active: bool = ..., override_other: bool = ..., override_latched: bool = ..., timeout: bool = ..., fault: bool = ..., bad_crc: bool = ..., bad_rc: bool = ..., degraded: bool = ..., limit_rate: _Optional[float] = ..., limit_value: _Optional[float] = ..., cmd_src: _Optional[_Union[_cmd_src_pb2.CmdSrc, _Mapping]] = ...) -> None: ...
