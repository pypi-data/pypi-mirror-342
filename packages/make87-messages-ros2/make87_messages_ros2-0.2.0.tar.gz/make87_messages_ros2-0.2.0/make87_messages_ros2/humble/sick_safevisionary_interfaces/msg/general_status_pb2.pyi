from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GeneralStatus(_message.Message):
    __slots__ = ["header", "run_mode_active", "device_error", "application_error", "sleep_mode", "wait_for_input", "wait_for_cluster", "contamination_warning", "contamination_error", "dead_zone_detection", "temperature_warning"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    RUN_MODE_ACTIVE_FIELD_NUMBER: _ClassVar[int]
    DEVICE_ERROR_FIELD_NUMBER: _ClassVar[int]
    APPLICATION_ERROR_FIELD_NUMBER: _ClassVar[int]
    SLEEP_MODE_FIELD_NUMBER: _ClassVar[int]
    WAIT_FOR_INPUT_FIELD_NUMBER: _ClassVar[int]
    WAIT_FOR_CLUSTER_FIELD_NUMBER: _ClassVar[int]
    CONTAMINATION_WARNING_FIELD_NUMBER: _ClassVar[int]
    CONTAMINATION_ERROR_FIELD_NUMBER: _ClassVar[int]
    DEAD_ZONE_DETECTION_FIELD_NUMBER: _ClassVar[int]
    TEMPERATURE_WARNING_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    run_mode_active: int
    device_error: int
    application_error: int
    sleep_mode: int
    wait_for_input: int
    wait_for_cluster: int
    contamination_warning: int
    contamination_error: int
    dead_zone_detection: int
    temperature_warning: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., run_mode_active: _Optional[int] = ..., device_error: _Optional[int] = ..., application_error: _Optional[int] = ..., sleep_mode: _Optional[int] = ..., wait_for_input: _Optional[int] = ..., wait_for_cluster: _Optional[int] = ..., contamination_warning: _Optional[int] = ..., contamination_error: _Optional[int] = ..., dead_zone_detection: _Optional[int] = ..., temperature_warning: _Optional[int] = ...) -> None: ...
