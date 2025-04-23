from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class ActiveMonitoringCase(_message.Message):
    __slots__ = ["monitoring_case_1", "monitoring_case_2", "monitoring_case_3", "monitoring_case_4"]
    MONITORING_CASE_1_FIELD_NUMBER: _ClassVar[int]
    MONITORING_CASE_2_FIELD_NUMBER: _ClassVar[int]
    MONITORING_CASE_3_FIELD_NUMBER: _ClassVar[int]
    MONITORING_CASE_4_FIELD_NUMBER: _ClassVar[int]
    monitoring_case_1: int
    monitoring_case_2: int
    monitoring_case_3: int
    monitoring_case_4: int
    def __init__(self, monitoring_case_1: _Optional[int] = ..., monitoring_case_2: _Optional[int] = ..., monitoring_case_3: _Optional[int] = ..., monitoring_case_4: _Optional[int] = ...) -> None: ...
