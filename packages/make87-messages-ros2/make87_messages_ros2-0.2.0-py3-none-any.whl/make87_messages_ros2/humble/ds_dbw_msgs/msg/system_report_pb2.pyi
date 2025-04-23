from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.ds_dbw_msgs.msg import system_state_pb2 as _system_state_pb2
from make87_messages_ros2.humble.ds_dbw_msgs.msg import system_sync_mode_pb2 as _system_sync_mode_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SystemReport(_message.Message):
    __slots__ = ["header", "ros2_header", "inhibit", "validate_cmd_crc_rc", "system_sync_mode", "state", "reason_disengage", "reason_not_ready", "reason_disengage_str", "reason_not_ready_str", "btn_enable", "btn_disable", "lockout", "override", "ready", "enabled", "fault", "bad_crc", "bad_rc"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    INHIBIT_FIELD_NUMBER: _ClassVar[int]
    VALIDATE_CMD_CRC_RC_FIELD_NUMBER: _ClassVar[int]
    SYSTEM_SYNC_MODE_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    REASON_DISENGAGE_FIELD_NUMBER: _ClassVar[int]
    REASON_NOT_READY_FIELD_NUMBER: _ClassVar[int]
    REASON_DISENGAGE_STR_FIELD_NUMBER: _ClassVar[int]
    REASON_NOT_READY_STR_FIELD_NUMBER: _ClassVar[int]
    BTN_ENABLE_FIELD_NUMBER: _ClassVar[int]
    BTN_DISABLE_FIELD_NUMBER: _ClassVar[int]
    LOCKOUT_FIELD_NUMBER: _ClassVar[int]
    OVERRIDE_FIELD_NUMBER: _ClassVar[int]
    READY_FIELD_NUMBER: _ClassVar[int]
    ENABLED_FIELD_NUMBER: _ClassVar[int]
    FAULT_FIELD_NUMBER: _ClassVar[int]
    BAD_CRC_FIELD_NUMBER: _ClassVar[int]
    BAD_RC_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    inhibit: bool
    validate_cmd_crc_rc: bool
    system_sync_mode: _system_sync_mode_pb2.SystemSyncMode
    state: _system_state_pb2.SystemState
    reason_disengage: int
    reason_not_ready: int
    reason_disengage_str: str
    reason_not_ready_str: str
    btn_enable: bool
    btn_disable: bool
    lockout: bool
    override: bool
    ready: bool
    enabled: bool
    fault: bool
    bad_crc: bool
    bad_rc: bool
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., inhibit: bool = ..., validate_cmd_crc_rc: bool = ..., system_sync_mode: _Optional[_Union[_system_sync_mode_pb2.SystemSyncMode, _Mapping]] = ..., state: _Optional[_Union[_system_state_pb2.SystemState, _Mapping]] = ..., reason_disengage: _Optional[int] = ..., reason_not_ready: _Optional[int] = ..., reason_disengage_str: _Optional[str] = ..., reason_not_ready_str: _Optional[str] = ..., btn_enable: bool = ..., btn_disable: bool = ..., lockout: bool = ..., override: bool = ..., ready: bool = ..., enabled: bool = ..., fault: bool = ..., bad_crc: bool = ..., bad_rc: bool = ...) -> None: ...
