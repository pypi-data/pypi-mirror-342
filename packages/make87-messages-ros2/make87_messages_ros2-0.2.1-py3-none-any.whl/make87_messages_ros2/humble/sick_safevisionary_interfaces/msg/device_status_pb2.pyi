from make87_messages.core import header_pb2 as _header_pb2
from make87_messages_ros2.humble.sick_safevisionary_interfaces.msg import active_monitoring_case_pb2 as _active_monitoring_case_pb2
from make87_messages_ros2.humble.sick_safevisionary_interfaces.msg import general_status_pb2 as _general_status_pb2
from make87_messages_ros2.humble.std_msgs.msg import header_pb2 as _header_pb2_1
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DeviceStatus(_message.Message):
    __slots__ = ["header", "ros2_header", "status", "general_status", "cop_safety_related", "cop_non_safety_related", "cop_reset_required", "active_monitoring_case", "contamination_level"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    ROS2_HEADER_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    GENERAL_STATUS_FIELD_NUMBER: _ClassVar[int]
    COP_SAFETY_RELATED_FIELD_NUMBER: _ClassVar[int]
    COP_NON_SAFETY_RELATED_FIELD_NUMBER: _ClassVar[int]
    COP_RESET_REQUIRED_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_MONITORING_CASE_FIELD_NUMBER: _ClassVar[int]
    CONTAMINATION_LEVEL_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    ros2_header: _header_pb2_1.Header
    status: int
    general_status: _general_status_pb2.GeneralStatus
    cop_safety_related: int
    cop_non_safety_related: int
    cop_reset_required: int
    active_monitoring_case: _active_monitoring_case_pb2.ActiveMonitoringCase
    contamination_level: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., ros2_header: _Optional[_Union[_header_pb2_1.Header, _Mapping]] = ..., status: _Optional[int] = ..., general_status: _Optional[_Union[_general_status_pb2.GeneralStatus, _Mapping]] = ..., cop_safety_related: _Optional[int] = ..., cop_non_safety_related: _Optional[int] = ..., cop_reset_required: _Optional[int] = ..., active_monitoring_case: _Optional[_Union[_active_monitoring_case_pb2.ActiveMonitoringCase, _Mapping]] = ..., contamination_level: _Optional[int] = ...) -> None: ...
