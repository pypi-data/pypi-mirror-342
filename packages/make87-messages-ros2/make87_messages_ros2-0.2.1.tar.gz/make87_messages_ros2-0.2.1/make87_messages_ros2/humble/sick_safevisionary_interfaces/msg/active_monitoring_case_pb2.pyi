from make87_messages.core import header_pb2 as _header_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ActiveMonitoringCase(_message.Message):
    __slots__ = ["header", "monitoring_case_1", "monitoring_case_2", "monitoring_case_3", "monitoring_case_4"]
    HEADER_FIELD_NUMBER: _ClassVar[int]
    MONITORING_CASE_1_FIELD_NUMBER: _ClassVar[int]
    MONITORING_CASE_2_FIELD_NUMBER: _ClassVar[int]
    MONITORING_CASE_3_FIELD_NUMBER: _ClassVar[int]
    MONITORING_CASE_4_FIELD_NUMBER: _ClassVar[int]
    header: _header_pb2.Header
    monitoring_case_1: int
    monitoring_case_2: int
    monitoring_case_3: int
    monitoring_case_4: int
    def __init__(self, header: _Optional[_Union[_header_pb2.Header, _Mapping]] = ..., monitoring_case_1: _Optional[int] = ..., monitoring_case_2: _Optional[int] = ..., monitoring_case_3: _Optional[int] = ..., monitoring_case_4: _Optional[int] = ...) -> None: ...
